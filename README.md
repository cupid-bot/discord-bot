# Cupid Discord Bot

This is the Discord Bot interface to the Cupid API.

## Installation

Dependencies:

- [Python 3.9+](https://www.python.org/downloads/) (Python 3.x where x >= 9)
- [Pipenv](https://pypi.org/project/pipenv/) (`python3 -m pip install pipenv`)

Once you have these dependencies installed:

1. **Create a virtual environment:** `python3 -m pipenv shell`
2. **Install dependencies:** `pipenv install`
3. **Optionally, install development dependencies:** `pipenv install -d`

## Configuration

You can configure the bot using a file named `config.ini`, placed in this
directory. You can also provide options in environment variables, but config
file settings will overwrite environment variable settings.

The following options are available:

| Name            | Default                            | Description                          |
|-----------------|------------------------------------|--------------------------------------|
| `cupid_token`   | *Required*                         | An app token for the Cupid API.      |
| `discord_token` | *Required*                         | A bot token for Discord.             |
| `cupid_api_url` | `https://cupid-api.artemisdev.xyz` | The base URL of the Cupid API.       |
| `prefix`        | `?`                                | The Discord command prefix.          |
| `guild_id`      | `839867213196427264`               | The ID of the Discord server to use. |
| `guild_name`    | `Polytics`                         | The name of the Discord server.      |
| `accent_colour` | `#ff2fd6`                          | Accent colour for bot embeds.        |

## Commands

The following commands are available:

- **Run the bot:** `pipenv run bot`
- **Lint code (requires dev dependecies):** `pipenv run lint`
