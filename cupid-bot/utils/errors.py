"""Discord.py command error handler."""
import re
import traceback

from cupid import CupidError

import discord
from discord.ext import commands


async def on_cupid_error(ctx: commands.Context, error: CupidError):
    """Handle a Cupid API error."""
    await ctx.send(embed=discord.Embed(
        color=0xd04040,
        title=error.description,
        description=error.message,
    ))


async def on_command_error(ctx: commands.Context, error: Exception):
    """Handle an error."""
    if hasattr(error, 'original') and isinstance(error.original, CupidError):
        await on_cupid_error(ctx, error.original)
        return
    raw_title = type(error).__name__
    raw_title = re.sub('([a-z])([A-Z])', r'\1 \2', raw_title)
    title = raw_title[0].upper() + raw_title[1:].lower()
    e = discord.Embed(
        colour=0xd04040, title=title, description=str(error),
    )
    await ctx.send(embed=e)
    if hasattr(error, 'original'):
        err = error.original
        traceback.print_tb(err.__traceback__)
        print(f'{type(err).__name__}: {err}')
