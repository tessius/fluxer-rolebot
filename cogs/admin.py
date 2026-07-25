import fluxer
from fluxer import Cog
from urllib.parse import urlparse

from util.admin import is_admin
from util.database import (
    add_configured_message,
    delete_configured_message,
    delete_all_configured_messages,
    get_configured_messages,
)
import logging

logger = logging.getLogger(__name__)


def _parse_message_link(link: str, guild_id: int) -> tuple[int, int, int] | str:
    """Parse a message link and return (guild_id, channel_id, message_id) or an error string."""
    parsed_link = urlparse(link)
    if not parsed_link.path:
        return "Invalid message link format."

    split_path = parsed_link.path.split("/")
    if len(split_path) < 5 or split_path[-4] != "channels":
        return "Invalid message link format."

    try:
        link_guild_id = int(split_path[-3])
        channel_id = int(split_path[-2])
        msg_id = int(split_path[-1])
    except ValueError:
        return "Invalid message link format."

    if link_guild_id != guild_id:
        return "The linked message must be in the same server."

    return (link_guild_id, channel_id, msg_id)


class Admin(Cog):
    def __init__(self, bot: fluxer.Bot):
        super().__init__(bot)

    @Cog.command()
    async def setmessage(self, ctx: fluxer.Message):
        """
        Add a message to the list of role reaction messages.
        Usage: `!setmessage <message_link>`
        Multiple messages can be registered; each is watched independently.
        """
        if ctx.guild_id is None:
            await ctx.reply("This command can only be used in a server.")
            return

        if not await is_admin(self.bot, ctx):
            await ctx.reply("You need administrator permissions to use this command.")
            return

        parts = ctx.content.split()
        if len(parts) < 2:
            await ctx.reply("Usage: `!setmessage <message_link>`")
            return

        result = _parse_message_link(parts[-1], ctx.guild_id)
        if isinstance(result, str):
            await ctx.reply(result)
            return

        _, channel_id, msg_id = result

        added = add_configured_message(ctx.guild_id, channel_id, msg_id)
        if not added:
            await ctx.reply(f"Message `{msg_id}` is already registered.")
            return

        await ctx.reply(f"Added role react message `{msg_id}` in <#{channel_id}>.")

    @Cog.command()
    async def removemessage(self, ctx: fluxer.Message):
        """
        Remove a specific role reaction message by link.
        Usage: `!removemessage <message_link>`
        Use `!removemessage all` to clear all registered messages.
        """
        if ctx.guild_id is None:
            await ctx.reply("This command can only be used in a server.")
            return

        if not await is_admin(self.bot, ctx):
            await ctx.reply("You need administrator permissions to use this command.")
            return

        parts = ctx.content.split()
        if len(parts) < 2:
            await ctx.reply(
                "Usage: `!removemessage <message_link>` or `!removemessage all`"
            )
            return

        arg = parts[-1]

        if arg.lower() == "all":
            removed = delete_all_configured_messages(ctx.guild_id)
            if removed:
                await ctx.reply("Removed all role react message configurations.")
            else:
                await ctx.reply("No role react messages are configured for this server.")
            return

        result = _parse_message_link(arg, ctx.guild_id)
        if isinstance(result, str):
            await ctx.reply(result)
            return

        _, channel_id, msg_id = result

        removed = delete_configured_message(ctx.guild_id, msg_id)
        if removed:
            await ctx.reply(
                f"Removed role react message `{msg_id}` in <#{channel_id}>."
            )
        else:
            await ctx.reply(
                f"Message `{msg_id}` was not found in the configured messages."
            )

    @Cog.command()
    async def listmessages(self, ctx: fluxer.Message):
        """
        List all configured role reaction messages for this server.
        Usage: `!listmessages`
        """
        if ctx.guild_id is None:
            await ctx.reply("This command can only be used in a server.")
            return

        if not await is_admin(self.bot, ctx):
            await ctx.reply("You need administrator permissions to use this command.")
            return

        messages = get_configured_messages(ctx.guild_id)
        if not messages:
            await ctx.reply("No role react messages are configured for this server.")
            return

        lines = ["**Configured role react messages:**"]
        for i, msg in enumerate(messages, 1):
            lines.append(
                f"{i}. Message `{msg['message_id']}` in <#{msg['channel_id']}>"
            )
        await ctx.reply("\n".join(lines))


async def setup(bot: fluxer.Bot):
    await bot.add_cog(Admin(bot))
