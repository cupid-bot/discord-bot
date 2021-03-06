"""Subclass of the Discord.py ext.commands bot for the Cupid bot."""
import typing

from cupid import Cupid, Gender, NotFoundError
from cupid.annotations import UserAsAppWithRelationships

import discord
from discord.ext import commands

from .config import CONFIG
from .utils import errors
from .utils.helpcmd import Help

if typing.TYPE_CHECKING:
    from .utils import Context


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
        try:
            self.load_extension('jishaku')
        except commands.ExtensionNotFound:
            pass
        self.load_extension('cupid-bot.cogs')
        self.run(CONFIG.discord_token)

    async def on_ready(self):
        """Create the Cupid App instance."""
        self.app = await self.cupid.app(CONFIG.cupid_token)
        print(f'Discord: Logged in as {self.user}.')
        print(f'Cupid API: Logged in as {self.app.name}.')
        print('----------')

    async def close(self):
        """Close the Discord and Cupid clients."""
        await self.cupid.close()
        await super().close()

    async def get_or_create_user(
            self, user: discord.User) -> UserAsAppWithRelationships:
        """Ensure sure that a user is registered."""
        try:
            cupid_user: UserAsAppWithRelationships = await self.app.get_user(
                user.id,
            )
        except NotFoundError:
            await self.app.create_user(
                id=user.id,
                name=user.name,
                discriminator=user.discriminator,
                avatar_url=str(user.avatar.url),
                gender=Gender.NON_BINARY,
            )
            return await self.app.get_user(user.id)
        else:
            await cupid_user.edit(
                name=user.name,
                discriminator=user.discriminator,
                avatar_url=str(user.avatar.url).split('?')[0],
            )
            return cupid_user

    async def global_check(self, ctx: 'Context') -> bool:
        """Register users and ensure commands are used in the right guild."""
        if (not ctx.guild) or ctx.guild.id != CONFIG.guild_id:
            raise commands.CommandError(
                f'This bot can only be used in **{CONFIG.guild_name}**.',
            )
        ctx.cupid_user = await self.get_or_create_user(ctx.author)
        return True

    async def on_user_update(self, before: discord.User, after: discord.User):
        """Keep users up to date with the API."""
        if after.bot:
            return
        await self.get_or_create_user(after)

    async def on_message(self, message: discord.Message):
        """Send the prefix if the bot is mentioned."""
        await super().on_message(message)
        me = message.guild.me if message.guild else self.user
        if me in message.mentions:
            await message.channel.send(f'My prefix is `{CONFIG.prefix}`.')

    async def on_command_error(self, ctx: 'Context', error: Exception):
        """Handle an error."""
        await errors.on_command_error(ctx, error)
