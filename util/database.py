from tinydb import TinyDB, Query
import os

Database = TinyDB(os.getenv("DB_PATH", "db.json"))
roles_table = Database.table("roles")
message_table = Database.table("message")


def set_role_association(guild_id: int, role_id: int, emoji: str) -> None:
    Guild = Query()
    roles_table.upsert(
        {"guild_id": guild_id, "role_id": role_id, "emoji": emoji},
        (Guild.guild_id == guild_id) & (Guild.emoji == emoji),
    )


def get_role_association(guild_id: int, emoji: str) -> int | None:
    Guild = Query()
    result = roles_table.search((Guild.guild_id == guild_id) & (Guild.emoji == emoji))
    return result[0]["role_id"] if result else None


def add_configured_message(guild_id: int, channel_id: int, message_id: int) -> bool:
    """Add a message to the list of configured role reaction messages.
    Returns False if the message is already registered, True if added."""
    Guild = Query()
    existing = message_table.search(
        (Guild.guild_id == guild_id) & (Guild.message_id == message_id)
    )
    if existing:
        return False
    message_table.insert(
        {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "message_id": message_id,
        }
    )
    return True


def get_configured_messages(guild_id: int) -> list[dict]:
    """Return all configured role reaction messages for a guild."""
    Guild = Query()
    return message_table.search(Guild.guild_id == guild_id)


def get_configured_message_by_id(guild_id: int, message_id: int) -> dict | None:
    """Return a single configured message entry by message ID."""
    Guild = Query()
    result = message_table.search(
        (Guild.guild_id == guild_id) & (Guild.message_id == message_id)
    )
    return result[0] if result else None


def delete_configured_message(guild_id: int, message_id: int) -> bool:
    """Remove a specific message from the configured role reaction messages."""
    Guild = Query()
    removed = message_table.remove(
        (Guild.guild_id == guild_id) & (Guild.message_id == message_id)
    )
    return len(removed) > 0


def delete_all_configured_messages(guild_id: int) -> bool:
    """Remove all configured role reaction messages for a guild."""
    Guild = Query()
    removed = message_table.remove(Guild.guild_id == guild_id)
    return len(removed) > 0


def delete_role_association(guild_id: int, emoji: str) -> bool:
    Guild = Query()
    removed = roles_table.remove(
        (Guild.guild_id == guild_id) & (Guild.emoji == emoji)
    )
    return len(removed) > 0


# ---------------------------------------------------------------------------
# Backwards-compat shims for any code that still calls the old single-message
# API. These map to the first registered message for the guild.
# ---------------------------------------------------------------------------

def set_configured_message(guild_id: int, channel_id: int, message_id: int) -> None:
    add_configured_message(guild_id, channel_id, message_id)


def get_configured_message(guild_id: int) -> dict | None:
    msgs = get_configured_messages(guild_id)
    if not msgs:
        return None
    return {"channel_id": msgs[0]["channel_id"], "message_id": msgs[0]["message_id"]}


def delete_configured_message_id(guild_id: int) -> bool:
    return delete_all_configured_messages(guild_id)
