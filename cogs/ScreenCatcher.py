import json
import time
import threading
import asyncio
import discord
from discord.ext import commands
import pytesseract
import pyautogui
import imagehash
from PIL import Image

global gamestart
gamestart = False

global roundstart
roundstart = False

global guild
guild = ""

global loop
loop = asyncio.get_event_loop()


class ScreenCatcher(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def newgame(self, ctx):
        global guild
        guild = ctx.message.guild
        global gamestart
        embed = discord.Embed(
            description="New game has been created\nPlease write %join to join",
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=embed)
        gamestart = True

    @commands.command()
    async def join(self, ctx):
        global gamestart
        if gamestart:
            with open('users.json', 'r') as f:
                loader = json.load(f)
            if len(loader["game"]) <= 10:
                author = ctx.message.author
                user_name = author.display_name
                user_id = author.id
                condition = False
                try:
                    if loader["game"][user_name] == user_id:
                        await ctx.message.author.send()
                        condition = False
                except:
                    condition = True
                    pass
                if condition:
                    loader["game"][user_name] = {
                        "id": user_id,
                        "Alive": True
                    }
                    embed = discord.Embed(
                        description="You have successfully joined the game!",
                        colour=discord.Colour.blue()
                    )
                    await author.send(embed=embed)
                    open("users.json", "w").write(
                        json.dumps(loader, sort_keys=True, indent=4, separators=(',', ': '))
                    )
            else:
                embed = discord.Embed(
                    description="There are already 10 people in the game!",
                    colour=discord.Colour.blue()
                )
                await ctx.send(embed=embed)
            await ctx.message.delete()
        else:
            await ctx.send("You must start a new game ``%newgame``")

    @commands.command()
    async def leave(self, ctx):
        global gamestart
        if gamestart:
            with open('users.json', 'r') as f:
                loader = json.load(f)
            user_name = ctx.message.author.name
            if loader["game"][user_name]["Alive"]:
                await ctx.message.author.send(embed=discord.Embed(
                    description="You're still Alive, you can't leave yet",
                    colour=discord.Colour.blue()
                ))
            else:
                loader["game"].pop(user_name, None)
                open("users.json", "w").write(
                    json.dumps(loader, sort_keys=True, indent=4, separators=(',', ': '))
                )
                await ctx.send(ctx.message.author.mention + " Has left the game!")
        else:
            await ctx.send("You must start a new game ``%newgame``")

    @leave.error
    async def leave_error(self, ctx, error):
        await ctx.send("You cannot leave a game you did not join")

    @commands.command(aliases=['startgame'])
    async def Start_Game(self, ctx):
        with open('users.json', 'r') as f:
            loader = json.load(f)
        if len(loader["game"]) < 1:
            await ctx.send(embed=discord.Embed(
                description="Minimum of 4 people are required to start a game",
                colour=discord.Colour.blue()
            ))
        else:
            channel = ctx.message.author.voice.channel
            global gamestart
            if gamestart:
                global roundstart
                roundstart = True
                asyncio.run_coroutine_threadsafe(await Start(), loop)
            else:
                await ctx.send("You must start a new game ``%newgame`` in order to start")


    @commands.command(aliases=["listjoined"])
    async def list_player(self, ctx):
        global gamestart
        if gamestart:
            sentence = ""
            with open('users.json', 'r') as f:
                data = json.load(f)
            count = 1
            for i in data["game"]:
                sentence += str(count) + ". " + i
                global roundstart
                if roundstart:
                    if data["game"][i]["Alive"]:
                        sentence += " (Status - Alive)\n"
                    else:
                        sentence += " (Status - Dead)\n"
                    s = "Round In Progress"
                else:
                    sentence += "\n"
                    s = "Round Haven't Started"
                count += 1
            embed = discord.Embed(
                title=s,
                description=sentence,
                colour=discord.Colour.blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, there is no game open, you can do so by typing %newgame")

    @commands.command()
    async def dead(self, ctx):
        global roundstart
        if not roundstart:
            await ctx.send(embed=discord.Embed(
                description="Game did not start yet",
                colour=discord.Colour.blue()
            ))
        else:
            user_id = ctx.message.author.id
            global guild
            member = guild.get_member(user_id)
            member.edit(mute=True)
            with open('users.json', 'r') as f:
                loader = json.load(f)
            if loader["game"][ctx.message.author.display_name]["Alive"]:
                loader["game"][ctx.message.author.display_name]["Alive"] = False
                open("users.json", "w").write(
                    json.dumps(loader, sort_keys=True, indent=4, separators=(',', ': '))
                )
                await ctx.send(ctx.message.author.mention + " died, " + str(CheckLeft()) + " Are left")
            else:
                await ctx.send("You are already dead!")


def setup(client):
    client.add_cog(ScreenCatcher(client))


async def Start():
    pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
    print("sequence started, enjoy!")
    ShhHash = imagehash.average_hash(Image.open('Images/Shhh.png'))
    DiscussHash = imagehash.average_hash(Image.open('Images/discuss.png'))
    EmergencyHash = imagehash.average_hash(Image.open('Images/Emergency.png'))
    VictoryHash = imagehash.average_hash(Image.open('Images/Victory.png'))
    DefeatHash = imagehash.average_hash(Image.open('Images/Defeat.png'))
    while True:
        myScreenshot = pyautogui.screenshot()
        hash = imagehash.average_hash(myScreenshot)

        # StartGame:
        if hash - ShhHash < 4:
            await MuteJoined()
            print("Game has began")
        # End---

        # Discuss:
        if hash - DiscussHash < 10 or hash - EmergencyHash < 10:
            print(hash - EmergencyHash)
            print("Started Discussion")
            await UnmuteAlive()
            await asyncio.sleep(2)
            SkeldHash = imagehash.average_hash(Image.open('Images/MapEjections/TheSkeldEjection.png'))
            PolusHash = imagehash.average_hash(Image.open('Images/MapEjections/PolusEjection.png'))
            MiraHash = imagehash.average_hash(Image.open('Images/MapEjections/MiraHQEjection.png'))
            while True:
                myScreenshot = pyautogui.screenshot()
                hash = imagehash.average_hash(myScreenshot)

                if hash - SkeldHash < 5 or hash - PolusHash < 5 or hash - MiraHash < 5:
                    await MuteJoined()
                    print("Stopped Discussion")
                    break
        # End---

        # Victory/Defeat
        if hash - VictoryHash < 5 or hash - DefeatHash < 5:
            await UnmuteAll()
            print("Game has ended")
            global roundstart
            roundstart = False
            resurrect()
            break


async def MuteJoined():
    with open('users.json', 'r') as f:
        loader = json.load(f)
    for i in loader["game"]:
        global guild
        user = guild.get_member(loader["game"][i]["id"])
        await user.edit(mute=True)


async def UnmuteAlive():
    with open('users.json', 'r') as f:
        loader = json.load(f)
    for i in loader["game"]:
        global guild
        if loader["game"][i]["Alive"]:
            user = guild.get_member(loader["game"][i]["id"])
            await user.edit(mute=False)


def CheckLeft():
    with open('users.json', 'r') as f:
        loader = json.load(f)
    count = 0
    for i in loader["game"]:
        if loader["game"][i]["Alive"]:
            count += 1
    return count


async def UnmuteAll():
    with open('users.json', 'r') as f:
        loader = json.load(f)
    global guild
    for i in loader["game"]:
        user = guild.get_member(loader["game"][i]["id"])
        await user.edit(mute=False)


def resurrect():
    with open('users.json', 'r') as f:
        loader = json.load(f)
    for i in loader["game"]:
        if not loader[i]["Alive"]:
            loader[i]["Alive"] = True

    open("users.json", "w").write(
        json.dumps(loader, sort_keys=True, indent=4, separators=(',', ': '))
    )