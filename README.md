# Cupid Discord Bot

This is the Discord Bot interface to the Cupid API.

## Installation

Dependencies:

- [Python 3.9+](https://www.python.org/downloads/) (Python 3.x where x >= 9)
- [Poetry](https://python-poetry.org/docs/master/#installation)

  Click the link for installation instructions, or:

  **\*nix:**
  `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -`

  **Windows Powershell:**
  `(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -`

Once you have these dependencies installed:

1. **Create a virtual environment:** `python3 -m poetry shell`
2. **Install dependencies:** `poetry install --no-dev`
   (remove `--no-dev` for development dependencies)

## Configuration

You can configure the bot using a file named `config.ini`, placed in this
directory. You can also provide options in environment variables, but config
file settings will overwrite environment variable settings.

The following options are available:

| Name            | Default                            | Description                          |
|-----------------|------------------------------------|--------------------------------------|
| `cupid_token`   | *Required*                         | An app token for the Cupid API.      |
| `discord_token` | *Required*                         | A bot token for Discord.             |
| `tenor_token`   | *Required*                         | An API token for Tenor.              |
| `cupid_api_url` | `https://cupid-api.artemisdev.xyz` | The base URL of the Cupid API.       |
| `prefix`        | `?`                                | The Discord command prefix.          |
| `guild_id`      | `839867213196427264`               | The ID of the Discord server to use. |
| `guild_name`    | `Polytics`                         | The name of the Discord server.      |
| `accent_colour` | `#ff2fd6`                          | Accent colour for bot embeds.        |

## Commands

The following commands are available:

- **Run the bot:** `poe bot`
- **Lint code (requires dev dependecies):** `poe lint`

Note that if to run outside of the Poetry shell (without running
`poetry shell`) you may have to replace `poe` with `poetry run poe` or even
`python3 -m poetry run poe`.
