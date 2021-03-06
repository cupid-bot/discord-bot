"""Discord.py command argument converters."""
import re
from typing import Optional

import cupid
from cupid import Gender
from cupid.annotations import UserAsAppWithRelationships

from discord.ext import commands
from discord.ext.commands.converter import MemberConverter
from discord.ext.commands.errors import BadArgument


class CupidUser(UserAsAppWithRelationships):
    """Converter for a Cupid user with relationship data."""

    @classmethod
    async def convert(
            cls,
            ctx: commands.Context,
            argument: str) -> UserAsAppWithRelationships:
        """Convert a user to a Cupid user."""
        try:
            member = await MemberConverter().convert(ctx, argument)
            return await ctx.bot.get_or_create_user(member)
        except BadArgument:
            try:
                id = int(argument.strip())
                return await ctx.bot.app.get_user(id)
            except (ValueError, cupid.NotFoundError):
                pass
            raise


class GenderConverter:
    """Converter for a user gender."""

    @classmethod
    async def convert(
            cls,
            ctx: commands.Context,
            raw_argument: str) -> Optional[Gender]:
        """Convert a raw argument to a user gender."""
        argument = re.sub('[_ -]', '', raw_argument.lower())
        if argument in ('nb', 'enby', 'nonbinary', 'neutral', 'neither'):
            return Gender.NON_BINARY
        if argument in ('f', 'female', 'girl', 'woman', 'lady'):
            return Gender.FEMALE
        if argument in ('m', 'male', 'boy', 'man', 'guy'):
            return Gender.MALE
        raise ValueError(
            f'Unkown gender {raw_argument!r}. Should be "non-binary", '
            '"female" or "male".',
        )
