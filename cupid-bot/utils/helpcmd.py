"""Discord.py help command."""
from typing import Any, Iterable

import discord
from discord.ext import commands


class Help(commands.DefaultHelpCommand):
    """Get help on the bot, a command or a command group.

    **__Understanding command usage:__**
    `[value]`: optional value
    `<value>`: required value
    `[value...]` or `[value]...`: multiple values
    `[value="default"]`: default value available.

    **__Values:__**
    A value can be anything without a space in it, eg. `text`,
    `@user`, `#channel`, `3`, `no`. If you want text with a space
    in it, do `"some text"`.

    **__Examples:__**
    `[p]help`
    `[p]help about`
    `[p]help Meta`
    """

    context: commands.Context

    def __init__(self, **options: Any):
        """Set up the help command."""
        options['command_attrs'] = {
            'aliases': ['h'],
            'help': self.__doc__,
            'brief': 'Shows this message.',
        }
        super().__init__(**options)

    def get_command_signature(
            self,
            command: commands.Command,
            ignore_aliases: bool = False) -> str:
        """Get a command signature, but optionally ignore aliases."""
        if command.aliases and not ignore_aliases:
            aliases = '|'.join(command.aliases)
            name = f'[{command.name}|{aliases}]'
        else:
            name = command.name
        if command.parent:
            name = f'{command.full_parent_name} {name}'
        return f'{self.context.clean_prefix}{name} {command.signature}'

    async def send_bot_help(
            self,
            cogs: dict[commands.Cog, Iterable[commands.Command]],
            description: str = '',
            title: str = 'Help'):
        """Send help for the entire bot."""
        e = discord.Embed(
            title=title, color=0x40d080, description=description,
        )
        for cog in cogs:
            if (not cog) or type(cog).__name__ == 'Jishaku':
                continue
            lines = []
            for command in await self.filter_commands(cog.walk_commands()):
                if command.hidden:
                    continue
                signature = self.get_command_signature(
                    command, ignore_aliases=True,
                )
                brief = command.brief or '???'
                line = f'**{signature}** *{brief}*'
                if line not in lines:     # Known bug where commands with
                    lines.append(line)    # aliases are duplicated.
            text = '\n'.join(lines)
            if text:
                e.add_field(name=cog.qualified_name, value=text, inline=False)
        await self.get_destination().send(embed=e)

    async def send_command_help(self, command: commands.Command):
        """Send help for a specific command."""
        desc = command.help or 'No description available.'
        desc = desc.replace('[p]', self.context.prefix)
        title = self.get_command_signature(command)
        e = discord.Embed(title=title, color=0x50C878, description=desc)
        await self.get_destination().send(embed=e)

    async def send_cog_help(self, cog: commands.Cog):
        """Send help for a specific cog."""
        await self.send_bot_help({cog: cog.walk_commands()})

    async def send_group_help(self, group: commands.Group):
        """Send help for a command group."""
        desc = group.help or 'No description available.'
        desc = desc.replace('[p]', self.context.prefix)
        await self.send_bot_help(
            {group: group.commands},
            description=desc,
            title=self.get_command_signature(group),
        )
