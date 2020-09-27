import json
import time

import discord
from discord.ext import commands
import pytesseract
import pyautogui
import imagehash
from PIL import Image

global gamestart
gamestart = False




class ScreenCatcher(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def newgame(self, ctx):
        global gamestart
        embed = discord.Embed(
            description="New game has been created\ndo %join in order to join",
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=embed)
        gamestart = True

    @commands.command()
    async def join(self, ctx):
        with open('users.json', 'r') as f:
            loader = json.load(f)
        if loader["game"].length <= 10:
            author = ctx.message.author
            user_name = author.name
            user_id = author.id
            loader["game"][user_name] = user_id
            embed = discord.Embed(
                description="You have successfully joined the game!",
                colour=discord.Colour.blue()
            )
            await author.send(embed=embed)
        else:
            embed = discord.Embed(
                description="There are already 10 people in the game!",
                colour=discord.Colour.blue()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        with open('users.json', 'r') as f:
            loader = json.load(f)
        user_name = await ctx.message.author.name
        loader["game"].pop(user_name, None)
        with open('users.json', 'w') as f:
            json.dump(loader, f)

    @leave.error
    async def leave_error(self, ctx, error):
        embed = discord.Embed(
            description="You cannot leave a game you did not join",
            colour=discord.Colour.red()
        )
        await ctx.message.author.send(embed=embed)

    @commands.command(aliases=['startgame'])
    async def Start_Game(self, ctx):
        channel = ctx.message.author.voice.channel
        global gamestart
        if gamestart:
            Start()
        else:
            await ctx.send("You must start a new game before being able to start the round")

    @Start_Game.error
    async def Start_Game_error(self, ctx, error):
        await ctx.send("You must be connected to the channel!")


def setup(client):
    client.add_cog(ScreenCatcher(client))


def Start():
    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
    while True:
        time.sleep(1)
        myScreenshot = pyautogui.screenshot()
        hash = imagehash.average_hash(myScreenshot)

        # Crewmate Alert
        otherhash = imagehash.average_hash(Image.open('Images/CrewmatePicked.png'))
        if hash - otherhash < 5:
            print("You are Crewmate")
        # End-------

        # Impostor Alert
        otherhash = imagehash.average_hash(Image.open('Images/Impostor.png'))
        if hash - otherhash < 5:
            print("You are Impostor!")
        # End-------

        # Discuss Alert
        otherhash = imagehash.average_hash(Image.open('Images/discuss.png'))
        if hash - otherhash < 10:
            print("Started Discussing")
            time.sleep(2)
            otherhash = imagehash.average_hash(Image.open('Images/vote.png'))
            while hash - otherhash < 10:
                time.sleep(1)
                hash = imagehash.average_hash(pyautogui.screenshot())
            print("Stopped Discussion")
        # End-------

        # Victory Alert
        otherhash = imagehash.average_hash(Image.open('Images/Victory.png'))
        if hash - otherhash < 10:
            print("You have won!")
            break
        # End--------

        # Defeat Alert
        otherhash = imagehash.average_hash(Image.open('Images/Defeat.png'))
        if hash - otherhash < 10:
            print("You have lost!")
            break
        # End--------
