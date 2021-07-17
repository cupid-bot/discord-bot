"""Cog for commands relating to users."""
from typing import Optional, TYPE_CHECKING

from cupid import NotFoundError
from cupid.annotations import UserAsApp

import discord
from discord.ext.commands import Cog, Context, command

from ..config import CONFIG

if TYPE_CHECKING:
    from ..bot import CupidBot


class People(Cog):
    """Commands relating to bot users."""

    def __init__(self, bot: 'CupidBot'):
        """Store a reference to the bot."""
        self.bot = bot

    @Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        """Update a user's information on the website when it changes."""
        try:
            user: UserAsApp = await self.bot.app.get_user(after.id)
        except NotFoundError:
            return
        await user.edit(
            name=after.name,
            discriminator=after.discriminator,
            avatar=after.avatar_url.split('?')[0],
        )

    @command(brief='View a profile.', aliases=['p'])
    async def profile(self, ctx: Context, *, user: Optional[discord.User]):
        """View a user's profile.

        Defaults to your own.

        Examples:
        `[p]profile`
        `[p]p @Artemis`
        """
        user = user or ctx.author
        try:
            user: UserAsApp = await self.bot.app.get_user(user.id)
        except NotFoundError:
            await ctx.send(f'User **{user.name}** is not registered.')
            return
        embed = discord.Embed(
            title=user.name,
            colour=CONFIG.accent_colour_int,
        )
        # TODO: Display user gender.
        # TODO: Add list of accepted relationships.
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    # TODO: Command to set gender.
    # TODO: Command to see relationship graph.
    # TODO: Command to see paginated list of people.
