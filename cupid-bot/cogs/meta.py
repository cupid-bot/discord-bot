"""The meta cog."""
import typing

import discord
from discord.ext import commands

from ..config import CONFIG

if typing.TYPE_CHECKING:
    from ..bot import CupidBot


class Meta(commands.Cog):
    """Commands relating to the bot itself."""

    def __init__(self, bot: 'CupidBot'):
        """Set the help command cog to this one."""
        self.bot = bot
        self.bot.help_command.cog = self
        self.bot.help_command.command_attrs = {'aliases': ['h']}

    @commands.command(brief='About the bot.')
    async def about(self, ctx: commands.Context):
        """Get some information about the bot."""
        embed = discord.Embed(
            title='About',
            description=ctx.bot.description,
            colour=CONFIG.accent_colour_int,
        )
        embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        embed.set_footer(text='By Artemis (artemisdev.xyz).')
        await ctx.send(embed=embed)
