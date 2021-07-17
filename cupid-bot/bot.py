"""Subclass of the Discord.py ext.commands bot for the Cupid bot."""
from cupid import Cupid

import discord
from discord.ext import commands

from .config import CONFIG
from .helpcmd import Help


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
        try:
            self.load_extension('jishaku')
        except ImportError:
            pass
        self.load_extension('cupid.cogs')
        self.run(CONFIG.discord_token)

    async def on_ready(self):
        """Create the Cupid App instance."""
        self.app = await self.cupid.app(CONFIG.cupid_token)

    async def close(self):
        """Close the Discord and Cupid clients."""
        await self.cupid.close()
        await super().close()
