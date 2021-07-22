"""Tool to get GIFs from the tenor API."""
import base64
import random

from cupid import Cupid, RelationshipKind
from cupid.annotations import Relationship

from ..config import CONFIG


TENOR_API = 'https://g.tenor.com/v1'


async def get_gif(cupid: Cupid, search: str) -> str:
    """Get the URL to a GIF.

    Uses the AIOHTTP session instance from Cupid client.
    """
    session = await cupid._get_client()  # noqa: SF01
    params = {
        'q': search,
        'contentfilter': 'low',
        'limit': 1,
        'key': CONFIG.tenor_token,
        # The endpoint always returns the same result if we don't do this,
        # because Tenor seems to seed the RNG on the request. This parameter
        # is not documented, but we just need to change the request each time.
        'rngseed': base64.b64encode(random.randbytes(64)).decode('utf-8'),
    }
    async with session.get(f'{TENOR_API}/random', params=params) as resp:
        data = await resp.json()
        return data['results'][0]['media'][0]['gif']['url']


async def proposal_gif(cupid: Cupid, relationship: Relationship) -> str:
    """Get the URL to a GIF to accompany a proposal."""
    if relationship.kind == RelationshipKind.MARRIAGE:
        term = 'proposal cute'
    else:
        term = 'hug child'
    return await get_gif(cupid, term)
