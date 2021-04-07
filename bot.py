# bot.py
import os
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from google_trans_new import google_translator  
load_dotenv()
TOKEN = os.getenv('WEATHERBOTTOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

bot = commands.Bot(command_prefix='!@#')

def get_schedule():
    newscasters = {
    'hiyama2018': "Saya Hiyama",
    'yuki': "Yuki Uchida",
    'matsu': "Matsu",
    'shirai': "Shirai",
    'nao': "Nao",
    'ailin': "Ailin",
    'komaki2018': "Komaki"
    }
    thumbnails = {
    'Saya Hiyama': "https://weathernews.jp/s/topics/img/caster/hiyama2018_m1.jpg",
    "Yuki Uchida": "https://weathernews.jp/s/topics/img/caster/yuki_m1.jpg"
    }
    page = requests.get("http://smtgvs.weathernews.jp/a/solive_timetable/timetable.json")
    timetable=page.json()
    outstring = ""
    embed = discord.Embed(title='WeatherNewsJP Schedule')
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

        time = strsplit[0].split(":")[1] + ":" + strsplit[0].split(":")[2] + " "
        title = strsplit[1].split(":")[1]
        caster = strsplit[2].split(":")[1]
        if caster == '':
            continue
        if caster in newscasters:
            caster = newscasters[strsplit[2].split(":")[1]]
        # if caster in thumbnails:
        #     caster += " " + thumbnails[caster]
        print(caster)
        translator = google_translator()
        # Staging for output string
        
        outstring += "Time schedule: " + time + " "
        outstring += "| " + translator.translate(title, lang_tgt='en') + " "
        outstring += "| Newscaster: " + caster + " "
        outstring += "\n"
        # print(strsplit)

    
        embed.add_field(name = 'Time', value= time, inline = True)
        embed.add_field(name = 'Title', value = translator.translate(title, lang_tgt='en'), inline = True)
        embed.add_field(name = 'Newscaster', value = caster, inline = True)

    return embed

#https://translate.google.com/translate?hl=&sl=ja&tl=en&u=https://weathernews.jp/s/solive24/timetable.html
@bot.command(name='schedule', help_command="hi")
async def schedule(ctx):
    # await ctx.send(get_schedule())
    await ctx.send(embed=get_schedule())

bot.run(TOKEN)