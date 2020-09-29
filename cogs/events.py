import json

import discord
from discord.ext import commands


class events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        deleteGame()
        print("Bot is ready!")


def setup(client):
    client.add_cog(events(client))


def deleteGame():
    with open("users.json", 'r') as f:
        loader = json.load(f)
    loader["game"] = {}
    open("users.json", "w").write(
        json.dumps(loader, sort_keys=True, indent=4, separators=(',', ': '))
    )
