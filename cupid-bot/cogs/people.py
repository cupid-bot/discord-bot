"""Cog for commands relating to users."""
from typing import Optional, TYPE_CHECKING

from cupid import RelationshipKind

import discord
from discord.ext.commands import Cog, Context, command

from .. import genders
from ..config import CONFIG
from ..converters import CupidUser, GenderConverter
from ..pagination import Paginator

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
        gender = genders.from_cupid(user.gender)
        # Not using str.title() because we want "Non-binary", not "Non-Binary".
        lines = [f'**{gender}**']
        for rel in user.accepted_relationships:
            if rel.kind == RelationshipKind.ADOPTION:
                if rel.initiator == user:
                    rel_name = gender.parent
                else:
                    rel_name = gender.child
            else:
                rel_name = gender.partner
            rel_to = rel.initiator if rel.other == user else rel.other
            lines.append(f' - **{rel_name.title()}** of **{rel_to.name}**')
        embed = discord.Embed(
            title=user.name,
            colour=CONFIG.accent_colour_int,
            description='\n'.join(lines),
        )
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @command(brief='Set your gender.')
    async def gender(self, ctx: Context, *, gender: GenderConverter):
        """Register your gender with the bot.

        Examples:
        `[p]gender non-binary`
        `[p]gender female`
        `[p]gender m`

        Note: at present, the bot only supports non-binary, female and male.
        """
        await ctx.cupid_user.edit(gender=gender)
        gender = genders.from_cupid(gender)
        await ctx.send(f'Set your gender to {gender}.')

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
                f'{genders.from_cupid(user.gender).emoji} {user.name}'
            ),
        ).setup()

    # TODO: Command to see relationship graph.
