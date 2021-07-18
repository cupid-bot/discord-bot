"""Utilities for dealing with user gender."""
from __future__ import annotations

import dataclasses

from cupid import Gender


@dataclasses.dataclass
class GenderData:
    """The options for user gender."""

    emoji: str
    name: str
    subjective: str
    objective: str
    possessive: str
    reflexive: str
    parent: str
    child: str
    partner: str

    def __str__(self) -> str:
        """Get a human readable title for the gender."""
        title = self.name[0].upper() + self.name[1:]
        return f'{self.emoji} {title}'


_BASE_EMOJI = '\N{HAPPY PERSON RAISING ONE HAND}'
_JOINER = '\N{ZERO WIDTH JOINER}'
_VARIATION = '\N{VARIATION SELECTOR-16}'

NON_BINARY = GenderData(
    emoji=_BASE_EMOJI,
    name='non-binary',
    subjective='they',
    objective='them',
    possessive='their',
    reflexive='themself',
    parent='parent',
    child='child',
    partner='partner',
)

FEMALE = GenderData(
    emoji=f'{_BASE_EMOJI}{_JOINER}\N{FEMALE SIGN}{_VARIATION}',
    name='female',
    subjective='she',
    objective='her',
    possessive='her',
    reflexive='herself',
    parent='mother',
    child='daughter',
    partner='wife',
)

MALE = GenderData(
    emoji=f'{_BASE_EMOJI}{_JOINER}\N{MALE SIGN}{_VARIATION}',
    name='male',
    subjective='he',
    objective='him',
    possessive='his',
    reflexive='himself',
    parent='father',
    child='son',
    partner='husband',
)


def from_cupid(value: Gender) -> GenderData:
    """Get information on a user's gender."""
    if value == Gender.NON_BINARY:
        return NON_BINARY
    elif value == Gender.FEMALE:
        return FEMALE
    elif value == Gender.MALE:
        return MALE
    else:
        raise ValueError(f'Unkown gender {value.name}.')
