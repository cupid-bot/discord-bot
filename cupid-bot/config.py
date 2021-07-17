"""Tool for parsing and exporting config options."""
from __future__ import annotations

import configparser
import os
import pathlib
import sys
from typing import Any

import pydantic
from pydantic.color import Color


class _Config(pydantic.BaseModel):
    """Config fields."""

    cupid_api_url: str = 'https://cupid-api.artemisdev.xyz'
    cupid_token: str
    discord_token: str
    prefix: str = '?'
    guild_id: int
    accent_colour: Color = '#ff2fd6'

    @property
    def accent_colour_int(self) -> int:
        """Get the accent colour as a number."""
        r, g, b = self.accent_colour.as_rgb_tuple(alpha=False)
        return r << 16 | g << 8 | b


class Config:
    """Mutable interface to config so that it can be shared between modules."""

    def __getattr__(self, key: str) -> Any:
        """Get a value from the underlying config."""
        return getattr(_CONFIG, key)


BASE_PATH = pathlib.Path(__file__).parent.parent
_CONFIG: _Config = None
CONFIG: _Config = Config()


def normalise_options(data: dict[str, Any]) -> dict[str, Any]:
    """Normalise config option keys."""
    return {
        key.lower().lstrip('-').replace('-', '_'): value
        for key, value in data.items()
    }


def _get_config_data() -> dict[str, Any]:
    """Get and combine raw config data."""
    data = normalise_options(os.environ)
    parser = configparser.ConfigParser()
    if parser.read(BASE_PATH / 'config.ini'):
        data.update(normalise_options(parser['cupid']))
    return data


def load():
    """Load config options."""
    global _CONFIG
    data = _get_config_data()
    try:
        _CONFIG = _Config(**data)
    except pydantic.ValidationError as error:
        print(f'Error parsing config:\n{error}')
        sys.exit(1)
