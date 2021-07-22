"""Utilities for commands and the bot."""
import typing

from discord.ext import commands

if typing.TYPE_CHECKING:
    from .converters import CupidUser
    from ..bot import CupidBot


class Context(commands.Context):
    """Command context with field for a Cupid user for the author.

    This exists to reduce type checking errors.
    """

    bot: 'CupidBot'
    cupid_user: 'CupidUser'
