import discord
from discord.ext.commands import AutoShardedBot


class Bot(AutoShardedBot):

    async def on_message(self, msg):
        if self.is_ready():
            return

        await self.process_commands(msg)