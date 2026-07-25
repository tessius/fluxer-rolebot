# fluxer-rolebot

A reaction role bot for [Fluxer](https://fluxer.app), forked from [PerpetualPossum/fluxer-rolebot](https://github.com/PerpetualPossum/fluxer-rolebot).

This is a modified version of the original with the following changes:

- **Multiple message support** — register more than one role reaction message per server. Each message is watched independently.
- **Self-hosted Fluxer support** — added `FLUXER_API_URL` environment variable to point the bot at your own Fluxer instance instead of the public `api.fluxer.app`.

> **Note:** This fork is intended for self-hosted Fluxer deployments. If you are looking for the original bot, see [PerpetualPossum/fluxer-rolebot](https://github.com/PerpetualPossum/fluxer-rolebot).

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

1. Copy `.env.example` to `.env` and fill in your bot token:

   ```
   cp .env.example .env
   ```

2. Install dependencies:

   ```
   uv sync
   ```

3. Run the bot:

   ```
   uv run main.py
   ```

### Docker

```
make build
make run
```

The bot stores data in a `data/` directory mounted as a volume. See the [Makefile](Makefile) for details.

## Commands

All commands currently require administrator permissions. The default prefix is `!` (configurable via `COMMAND_PREFIX`).

| Command | Description |
|---|---|
| `!setmessage <message_link>` | Add a message to the role reaction list. Can be run multiple times to register multiple messages |
| `!removemessage <message_link>` | Remove a specific role reaction message |
| `!removemessage all` | Remove all configured role reaction messages |
| `!listmessages` | List all configured role reaction messages |
| `!add @Role <emoji>` | Associate an emoji with a role (uses the only registered message if there's one) |
| `!add @Role <emoji> <message_link>` | Associate an emoji with a role on a specific message (required when multiple are registered) |
| `!remove <emoji>` | Remove an emoji-role association |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `FLUXER_TOKEN` | *(required)* | Bot token from your Fluxer instance |
| `FLUXER_API_URL` | `https://api.fluxer.app/v1` | API base URL — set this to your self-hosted instance (e.g. `https://chat.example.com/api/v1`) |
| `PREFIX_TYPE` | `default` | Can be `spaced` or `default`. Default: `<prefix>setmessage`, Spaced: `<prefix> setmessage` |
| `COMMAND_PREFIX` | `!` | Prefix for bot commands |
| `DB_PATH` | `db.json` | Path to the TinyDB database file |
