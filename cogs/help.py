from discord.ext import commands
import discord


class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Commands",
            description="%newgame - This is used to create a new game!\n%join - Join a game\n%leave - Leave a game (Once the game start you won't be able to leave until you die"
                        "\n%dead - If you're dead and write it the bot will not unmute you.\n%status - the status of current game",
            colour=discord.Colour.blue()
        )
        await ctx.message.author.send(embed=embed)


def setup(client):
    client.add_cog(help(client))
