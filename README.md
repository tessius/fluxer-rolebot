# fluxer-rolebot

A reaction role bot for [Fluxer](https://fluxer.app). Administrators configure one or more messages and associate emojis with roles. When users react, they automatically receive or lose the corresponding role. Multiple role reaction messages are supported — each message is watched independently.

Want to use this without hosting?

[Invite Here](https://web.fluxer.app/oauth2/authorize?client_id=1472276231307042825&scope=bot&permissions=1342377024)

[Support Server](https://fluxer.gg/kOPptC9Q)

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

| Command                          | Description                                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------------------------ |
| `!setmessage <message_link>`     | Add a message to the role reaction list. Can be run multiple times to register multiple messages |
| `!removemessage <message_link>`  | Remove a specific role reaction message                                                          |
| `!removemessage all`             | Remove all configured role reaction messages                                                     |
| `!listmessages`                  | List all configured role reaction messages                                                       |
| `!add @Role <emoji>`             | Associate an emoji with a role (uses the only registered message if there's one)                 |
| `!add @Role <emoji> <message_link>` | Associate an emoji with a role on a specific message (required when multiple are registered)  |
| `!remove <emoji>`                | Remove an emoji-role association                                                                 |

## Environment Variables

| Variable         | Default      | Description                                                                                                                            |
| ---------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `FLUXER_TOKEN`   | _(required)_ | Bot token from Fluxer                                                                                                                  |
| `PREFIX_TYPE`    | `default`    | Can be `spaced` or `default`. Default has the format `<prefix>setmessage` for example, and Spaced has the format `<prefix> setmessage` |
| `COMMAND_PREFIX` | `!`          | Prefix for bot commands                                                                                                                |
| `DB_PATH`        | `db.json`    | Path to the TinyDB database file                                                                                                       |
