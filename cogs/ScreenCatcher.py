import time

from discord.ext import commands
import pytesseract
import pyautogui
import imagehash
from PIL import Image

class ScreenCatcher(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def CatchWord(self, ctx):
        print("Sequence has started")
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





def setup(client):
    client.add_cog(ScreenCatcher(client))