# bot.py
import os
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('WEATHERBOTTOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

bot = commands.Bot(command_prefix='!@#')

def get_schedule():
    page = requests.get("http://smtgvs.weathernews.jp/a/solive_timetable/timetable.json")
    timetable=page.json()
    outstring = ""
    for schedule in timetable:
        test = ""
        strsplit = str(schedule).split(",")

        # Removing unwanted characters
        for count, string in enumerate(strsplit):
            string = string.replace(' ', '')
            string = string.replace('{', '')
            string = string.replace('}', '')
            string = string.replace('\'', '')
            strsplit[count] = string

        # Staging for output
        outstring += "Hour: " + strsplit[0].split(":")[1] + ":" + strsplit[0].split(":")[2] + " "
        outstring += "Title: " + strsplit[1].split(":")[1] + " "
        outstring += "Caster: " + strsplit[2].split(":")[1] + " "
        outstring += "\n"
        # print(strsplit)

    return outstring
#https://translate.google.com/translate?hl=&sl=ja&tl=en&u=https://weathernews.jp/s/solive24/timetable.html
@bot.command(name='schedule')
async def nine_nine(ctx):
    # page = requests.get("http://smtgvs.weathernews.jp/a/solive_timetable/timetable.json")
    # print(page.content)

    # soup = BeautifulSoup(page.content)
    # print(soup.prettify())
    # print(outstring)
    await ctx.send(get_schedule())

bot.run(TOKEN)