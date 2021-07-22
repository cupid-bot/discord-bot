"""Tools for forming specific sentences for generic concepts."""
from __future__ import annotations

import dataclasses

from cupid import Gender, RelationshipKind
from cupid.annotations import (
    Relationship,
    UserAsAppWithRelationships as User,
)


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


def get_gender_data(value: Gender) -> GenderData:
    """Get information on a user's gender."""
    if value == Gender.NON_BINARY:
        return NON_BINARY
    elif value == Gender.FEMALE:
        return FEMALE
    elif value == Gender.MALE:
        return MALE
    else:
        raise ValueError(f'Unkown gender {value.name}.')


def _get_opposite(user: User, relationship: Relationship) -> User:
    """Get the opposite user in a relationship."""
    if user == relationship.initiator:
        return relationship.other
    else:
        return relationship.initiator


def gender(user: User) -> str:
    """Get a string to display a user's gender."""
    gender = get_gender_data(user.gender)
    return f'{gender.emoji} **{gender.name[0].upper()}{gender.name[1:]}**'


def relationship_to(user: User, relationship: Relationship) -> str:
    """Get a bullet point summary of a user's relationship to another."""
    gender = get_gender_data(user.gender)
    if relationship.kind == RelationshipKind.ADOPTION:
        if relationship.initiator == user:
            name = gender.parent
        else:
            name = gender.child
    else:
        name = gender.partner
    opposite = _get_opposite(user, relationship)
    return f' - **{name.title()}** of **{opposite.name}**'


def relationship_announcement(relationship: Relationship) -> str:
    """Announce a relationship."""
    if relationship.kind == RelationshipKind.MARRIAGE:
        rel = 'is married to'
    else:
        rel = 'has adopted'
    return (
        f'<@{relationship.initiator.id}> {rel} <@{relationship.other.id}>!!!'
    )


def rejection_confirmation(relationship: Relationship) -> str:
    """Get a confirmation message when someone rejects a relationship."""
    kind = relationship.kind.value
    return f"You rejected {relationship.initiator.name}'s {kind} proposal."


def proposal_announcement(relationship: Relationship) -> str:
    """Announce a proposal."""
    if relationship.kind == RelationshipKind.MARRIAGE:
        action = 'proposes to'
    else:
        action = 'wants to adopt'
    return (
        f'{relationship.initiator.name} {action} {relationship.other.name}! '
        '\N{SMILING FACE WITH SMILING EYES AND THREE HEARTS}'
    )


def proposal_delete_confirmation(
        user: User, relationship: Relationship) -> str:
    """Get a confirmation message when someone deletes a proposal."""
    if relationship.kind == RelationshipKind.MARRIAGE:
        kind = 'marrying'
    else:
        kind = 'adopting'
    if relationship.initiator == user:
        action = 'cancelled'
        initiator = 'your'
        other_name = f'<@{relationship.other.id}>'
    else:
        action = 'rejected'
        initiator = f"<@{relationship.initiator.id}>\'s"
        other_name = 'you'
    return f'You {action} {initiator} proposal of {kind} {other_name}.'


def accepted_delete_confirmation(
        user: User, relationship: Relationship) -> str:
    """Confirm someone deleting an accepted relationship."""
    if relationship.initiator == user:
        opposite = relationship.other
    else:
        opposite = relationship.initiator
    gender = get_gender_data(opposite.gender)
    if relationship.kind == RelationshipKind.MARRIAGE:
        action = 'divorced'
        opposite_name = gender.partner
    else:
        if relationship.initiator == user:
            action = 'disowned'
            opposite_name = gender.child
        else:
            action = 'left'
            opposite_name = gender.parent
    return f'You {action} your {opposite_name}, <@{opposite.id}>.'


def delete_confirmation(user: User, relationship: Relationship) -> str:
    """Get a confirmation message when someone deletes a relationship."""
    if relationship.accepted:
        return accepted_delete_confirmation(user, relationship)
    else:
        return proposal_delete_confirmation(user, relationship)


def incoming_proposals(user: User) -> str:
    """Get a summary of a user's incoming proposals."""
    proposals = user.incoming_proposals
    if not proposals:
        return '*No proposals.*'
    lines = []
    for proposal in proposals:
        if proposal.kind == RelationshipKind.MARRIAGE:
            action = 'Marriage with'
        else:
            action = 'Adoption by'
        other = proposal.initiator
        lines.append(f'{action} <@{other.id}> ({other.name}).')
    return '\n'.join(lines)


def outgoing_proposals(user: User) -> str:
    """Get a summary of a user's outgoing proposals."""
    proposals = user.outgoing_proposals
    if not proposals:
        return '*No proposals.*'
    lines = []
    for proposal in proposals:
        if proposal.kind == RelationshipKind.MARRIAGE:
            action = 'Marriage with'
        else:
            action = 'Adoption of'
        other = proposal.other
        lines.append(f'{action} <@{other.id}> ({other.name}).')
    return '\n'.join(lines)
