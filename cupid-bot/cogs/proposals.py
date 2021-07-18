"""Cog for commands relating to relationships."""
from typing import TYPE_CHECKING

from discord.ext.commands import Cog

if TYPE_CHECKING:
    from ..bot import CupidBot


class Proposals(Cog):
    """Commands relating to relationships."""

    def __init__(self, bot: 'CupidBot'):
        """Store a reference to the bot."""
        self.bot = bot

    # TODO: Command to propose to someone.
    # TODO: Command to delete a relationship.
    #       Aliased to cancel, reject, leave, divorce, disown.
    # TODO: Command to accept a relationship.
    # TODO: Command to see your pending proposals.
