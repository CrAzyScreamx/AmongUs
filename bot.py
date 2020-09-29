import discord
import os
from discord.ext import commands
import json

client = commands.Bot(command_prefix=commands.when_mentioned_or("%"), case_insensitive=True)
client.remove_command('help')


def token_read():
    with open("token.json", "r") as f:
        loader = json.load(f)
    return loader["token"]


token = token_read()


@client.command()
async def re(ctx):
    if ctx.author.id == 231405897820143616:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.reload_extension(f'cogs.{filename[:-3]}')
        msg = ctx.message
        await msg.delete()
        await ctx.author.send("Extensions loaded")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
