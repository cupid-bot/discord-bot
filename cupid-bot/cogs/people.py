"""Cog for commands relating to users."""
from typing import Optional, TYPE_CHECKING

import discord
from discord.ext.commands import Cog, command

from ..config import CONFIG
from ..utils import Context
from ..utils.converters import CupidUser, GenderConverter
from ..utils.graph import render_graph
from ..utils.pagination import Paginator
from ..utils.sentences import (
    gender,
    get_gender_data,
    relationship_to,
)

if TYPE_CHECKING:
    from ..bot import CupidBot


class People(Cog):
    """Commands relating to bot users."""

    def __init__(self, bot: 'CupidBot'):
        """Store a reference to the bot."""
        self.bot = bot

    @command(brief='View a profile.', aliases=['p'])
    async def profile(self, ctx: Context, *, user: CupidUser = None):
        """View a user's profile.

        Defaults to your own.

        Examples:
        `[p]profile`
        `[p]p @Artemis`
        """
        user = user or ctx.cupid_user
        lines = [gender(user)]
        for relationship in user.accepted_relationships:
            lines.append(relationship_to(user, relationship))
        embed = discord.Embed(
            title=user.name,
            colour=CONFIG.accent_colour_int,
            description='\n'.join(lines),
        )
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @command(brief='Set your gender.')
    async def gender(self, ctx: Context, *, new_gender: GenderConverter):
        """Register your gender with the bot.

        Examples:
        `[p]gender non-binary`
        `[p]gender female`
        `[p]gender m`

        Note: at present, the bot only supports non-binary, female and male.
        """
        await ctx.cupid_user.edit(gender=new_gender)
        gender_name = gender(ctx.cupid_user)
        await ctx.send(f'Set your gender to {gender_name}.')

    @command(brief='See a list of people.', aliases=['people', 'l', 'search'])
    async def list(self, ctx: Context, *, search: Optional[str] = None):
        """Get a list of people registered, optionally with a search.

        Examples:
        `[p]list`
        `[p]search Rob`
        """
        users = self.bot.app.users(search=search)
        await users.get_page(0)    # Fetch a page to load metadata.
        await Paginator(
            ctx=ctx,
            title='People',
            page_count=users.total_pages,
            get_page=users.get_page,
            formatter=lambda user: (
                f'{get_gender_data(user.gender).emoji} {user.name}'
            ),
        ).setup()

    @command(brief='See a family tree.')
    async def tree(self, ctx: Context):
        """See a family tree with every person.

        Examples:
        `[p]tree`
        """
        graph = await self.bot.app.graph()
        file = render_graph(graph)
        await ctx.send(file=discord.File(file, filename='tree.png'))
