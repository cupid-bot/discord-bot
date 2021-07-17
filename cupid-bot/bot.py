"""Subclass of the Discord.py ext.commands bot for the Cupid bot."""
from cupid import Cupid, Gender, NotFoundError
from cupid.annotations import UserAsApp

import discord
from discord.ext import commands

from . import errors
from .config import CONFIG
from .helpcmd import Help


DESCRIPTION = (
    'Cupid Bot is responsible for managing all your marriage and adoption '
    'needs.'
)


class CupidBot(commands.Bot):
    """Bot class for the Cupid bot."""

    def __init__(self):
        """Set up the bot."""
        intents = discord.Intents.none()
        intents.messages = True
        intents.guilds = True
        intents.members = True
        intents.guild_reactions = True
        super().__init__(
            CONFIG.prefix,
            help_command=Help(),
            description=DESCRIPTION,
            intents=discord.Intents(
                messages=True,
                guild_reactions=True,
                guilds=True,
                members=True,
            ),
        )
        self.cupid = Cupid(CONFIG.cupid_api_url)
        self.add_check(self.global_check)
        for listener in (
                self.on_user_update, self.on_message, self.on_command_error):
            self.add_listener(listener)
        try:
            self.load_extension('jishaku')
        except ImportError:
            pass
        self.load_extension('cupid.cogs')
        self.run(CONFIG.discord_token)

    async def on_ready(self):
        """Create the Cupid App instance."""
        self.app = await self.cupid.app(CONFIG.cupid_token)

    async def close(self):
        """Close the Discord and Cupid clients."""
        await self.cupid.close()
        await super().close()

    async def get_or_create_user(self, user: discord.User) -> UserAsApp:
        """Ensure sure that a user is registered."""
        try:
            user: UserAsApp = await self.app.get_user(user.id)
        except NotFoundError:
            return await self.app.create_user(
                id=user.id,
                name=user.name,
                discord=user.discriminator,
                avatar_url=user.avatar_url,
                gender=Gender.NON_BINARY,
            )
        else:
            await user.edit(
                name=user.name,
                discriminator=user.discriminator,
                avatar_url=user.avatar_url.split('?')[0],
            )
            return user

    async def global_check(self, ctx: commands.Context) -> bool:
        """Register users and ensure commands are used in the right guild."""
        if (not ctx.guild) or ctx.guild.id != CONFIG.guild_id:
            raise commands.CommandError(
                f'This bot can only be used in **{CONFIG.guild_name}**.',
            )
        ctx.cupid_user = await self.get_or_create_user(ctx.author)

    async def on_user_update(self, ctx: commands.Context):
        """Keep users up to date with the API."""
        if ctx.author.bot:
            return
        await self.get_or_create_user(ctx.author)

    async def on_message(self, message: discord.Message):
        """Send the prefix if the bot is mentioned."""
        me = message.guild.me if message.guild else self.bot.user
        if me in message.mentions:
            await message.channel.send(f'My prefix is `{CONFIG.prefix}`.')

    async def on_command_error(self, ctx: commands.Context, error: Exception):
        """Handle an error."""
        await errors.on_command_error(ctx, error)
