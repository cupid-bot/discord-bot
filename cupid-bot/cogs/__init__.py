"""Discord.py command cogs for Cupid collated into an extension."""
from discord.ext import commands

from .meta import Meta
from .people import People
from .relationships import Relationships


COGS = [Meta, People, Relationships]


def setup(bot: commands.Bot):
    """Load the cogs."""
    for cog in COGS:
        cog = cog(bot)
        bot.add_cog(cog)
