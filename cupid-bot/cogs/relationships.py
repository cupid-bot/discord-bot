"""Cog for commands relating to relationships."""
from typing import Any, Callable, Coroutine, TYPE_CHECKING

from cupid import ForbiddenError, RelationshipKind
from cupid.annotations import OwnRelationship

from discord import ButtonStyle, Embed, Interaction
from discord.ext.commands import Cog, command
from discord.ui import Button, View, button

from ..config import CONFIG
from ..utils import Context
from ..utils.converters import CupidUser
from ..utils.gifs import proposal_gif
from ..utils.sentences import (
    delete_confirmation,
    incoming_proposals,
    outgoing_proposals,
    proposal_announcement,
    rejection_confirmation,
    relationship_announcement,
)

if TYPE_CHECKING:
    from ..bot import CupidBot


class ProposalView(View):
    """A view that allows a user to accept or a reject a proposal."""

    children: list[Button]

    def __init__(self, proposal: OwnRelationship):
        """Set up the view buttons."""
        self.proposal = proposal
        super().__init__(timeout=None)

    async def on_button(
            self,
            interaction: Interaction,
            callback: Callable[[], Coroutine[Any, Any, None]]) -> bool:
        """Handle either button being pressed.

        Return value indicates whether or not it was successful.
        """
        if (
                self.proposal.accepted
                or interaction.user.id != self.proposal.other.id):
            await interaction.response.send_message(
                'This proposal is not to you.', ephemeral=True,
            )
            return False
        try:
            await callback()
        except ForbiddenError as error:
            await interaction.response.send_message(str(error), ephemeral=True)
            return False
        await interaction.response.edit_message(view=None)
        return True

    @button(label='Accept', style=ButtonStyle.success, emoji='\N{TWO HEARTS}')
    async def accept(self, button: Button, interaction: Interaction):
        """Handle the user pressing the accept button."""
        if not await self.on_button(interaction, self.proposal.accept):
            return
        await interaction.followup.send(relationship_announcement(
            self.proposal,
        ))

    @button(label='Reject', style=ButtonStyle.danger, emoji='\N{BROKEN HEART}')
    async def reject(self, button: Button, interaction: Interaction):
        """Handle the user pressing the reject button."""
        if not await self.on_button(interaction, self.proposal.delete):
            return
        await interaction.followup.send(
            rejection_confirmation(self.proposal), ephemeral=True,
        )


class Relationships(Cog):
    """Commands relating to relationships."""

    def __init__(self, bot: 'CupidBot'):
        """Store a reference to the bot."""
        self.bot = bot

    async def propose_either(
            self, ctx: Context, to: CupidUser, kind: RelationshipKind):
        """Handle a proposal of marriage or adoption."""
        await ctx.cupid_user.propose(to, kind)
        proposal = await to.relationship(ctx.cupid_user)
        await ctx.send(
            f'<@{to.id}>',
            embed=Embed(
                title=proposal_announcement(proposal),
                color=CONFIG.accent_colour_int,
            ).set_footer(
                text=(
                    'If the buttons timeout, you can use '
                    f'"{ctx.prefix}accept @{ctx.author}" or '
                    f'"{ctx.prefix}reject @{ctx.author}".'
                ),
            ).set_image(
                url=await proposal_gif(self.bot.cupid, proposal),
            ),
            view=ProposalView(proposal),
        )

    @command(brief='Propose to someone.')
    async def propose(self, ctx: Context, *, to: CupidUser):
        """Propose marriage to another user.

        Example:
        `[p]propose @Artemis`
        """
        await self.propose_either(ctx, to, RelationshipKind.MARRIAGE)

    @command(brief='Adopt someone.')
    async def adopt(self, ctx: Context, *, to: CupidUser):
        """Propose adoption of another user.

        Example:
        `[p]adopt @Artemis`
        """
        await self.propose_either(ctx, to, RelationshipKind.ADOPTION)

    @command(brief='Accept a proposal.')
    async def accept(self, ctx: Context, *, other: CupidUser):
        """Accept a proposal from another user.

        Example:
        `[p]accept @Artemis`
        """
        relationship = await ctx.cupid_user.relationship(other)
        await relationship.accept()
        await ctx.send(relationship_announcement(relationship))

    @command(
        brief='Leave a relationship.',
        aliases=['cancel', 'reject', 'divorce', 'disown'],
    )
    async def leave(self, ctx: Context, *, other: CupidUser):
        """Leave/cancel/reject a relationship with another user.

        This can be used to cancel a proposal, reject a proposal, divorce
        someone you're married to, disown someone you've adopted or leave
        someone who's adopted you.

        Examples:
        `[p]leave @Bia`
        `[p]cancel @Charis`
        `[p]reject @Demeter`
        `[p]divorce @Eris`
        `[p]disown @Flora`
        """
        relationship = await ctx.cupid_user.relationship(other)
        await relationship.delete()
        await ctx.send(delete_confirmation(ctx.cupid_user, relationship))

    @command(brief='See your proposals.')
    async def proposals(self, ctx: Context):
        """See a list of all your incoming and outgoing proposals.

        Example:
        `[p]proposals`
        """
        await ctx.send(
            embed=Embed(
                title='Proposals',
                color=CONFIG.accent_colour_int,
            ).set_author(
                name=ctx.cupid_user.name,
                icon_url=ctx.cupid_user.avatar_url,
            ).add_field(
                name='Incoming',
                value=incoming_proposals(ctx.cupid_user),
                inline=False,
            ).add_field(
                name='Outgoing',
                value=outgoing_proposals(ctx.cupid_user),
                inline=False,
            ),
        )
