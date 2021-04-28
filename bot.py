# bot.py
import os
import requests
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from google_trans_new import google_translator  
from datetime import datetime, time, timedelta
import asyncio
import pytz

load_dotenv()
TOKEN = os.getenv('WEATHERBOTTOKEN')


INTERVAL = 2
CHANNEL = 829244449195294731
MESSAGE = "Test interval message"


bot = commands.Bot(command_prefix='!@#')

# async def list_guilds():
#     await bot.wait_until_ready()
#     print("** Weather Bot is Online **")
#     for guild in bot.guilds:
#         print('Active guilds: ' + str(guild.name))
#     await asyncio.sleep(600)

async def send_interval_message():
    await bot.wait_until_ready()
    channel = CHANNEL
    interval = INTERVAL
    message = MESSAGE
    WHEN = time(16, 0, 0) # UTC+0 but midnight in UTC+8 cause I don't know how to change offset :(
    now = datetime.utcnow()
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds) 
    # print("Sending interval message...")
    while True:
        now = datetime.utcnow()
        target_time = datetime.combine(now.date(), WHEN)
        seconds_until_target = (target_time - now).total_seconds()
        # await bot.get_channel(channel).send(message)
        print("Now: " + str(now) + " Target time: " + str(target_time) + " Seconds target: " + str(seconds_until_target))
        await asyncio.sleep(interval)
        await schedule(bot.get_channel(channel))

# bot.loop.create_task(list_guilds())
# print the active bot details to console 
@bot.event
async def on_ready():
    messageinterval = INTERVAL
    messagechannel = CHANNEL
    messagecontent = MESSAGE
    # you can customize the output message(s) below
    print('Message sent every: ' + str(messageinterval) + ' sec.')
    print('Destination channel id: ' + str(messagechannel))
    print('Message content: ' + str(messagecontent))
    bot.loop.create_task(send_interval_message())

def get_schedule():
    # Names from https://weathernews.jp/wnl/caster/
    newscasters = {
    'hiyama2018': "Saya Hiyama",
    'yuki': "Yuki Uchida",
    'matsu': "Ayaka Matsuyuki",
    'shirai': "Yukari Shirai",
    'nao': "Naoko Kakuta",
    'ailin': "Ailin Yamagishi",
    'komaki2018': "Yui Komaki",
    "sayane": "Sayane Egawa",
    "ayame": "Ayame Muto",
    "takayama": "Nana Takayama"
    }
    thumbnails = {
    'Saya Hiyama': "https://weathernews.jp/s/topics/img/caster/hiyama2018_m1.jpg",
    "Yuki Uchida": "https://weathernews.jp/s/topics/img/caster/yuki_m1.jpg"
    }
    page = requests.get("http://smtgvs.weathernews.jp/a/solive_timetable/timetable.json")
    timetable=page.json()
    embed = discord.Embed(title='Weather News Japan Live Stream Schedule')
    timestring = ""
    titlestring = ""
    casterstring = ""
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

        timestring += time + "\n"
        titlestring += translator.translate(title, lang_tgt='en') + "\n"
        casterstring += caster + "\n"
        # print(strsplit)

    
    embed.add_field(name = 'Time UTC+9', value= timestring, inline = True)
    embed.add_field(name = 'News Program', value = titlestring, inline = True)
    embed.add_field(name = 'Newscaster', value = casterstring, inline = True)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Weathernews_logo.svg/1024px-Weathernews_logo.svg.png")
    embed.set_footer(text='Weather News Schedule | Brought to you by Weather News JP Enthusiasts',icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Weathernews_logo.svg/1024px-Weathernews_logo.svg.png")
    return embed

#https://translate.google.com/translate?hl=&sl=ja&tl=en&u=https://weathernews.jp/s/solive24/timetable.html
@bot.command(name='schedule', help_command="hi")
async def schedule(ctx):
    # await ctx.send(get_schedule())
    await ctx.send(embed=get_schedule())
    page = requests.get("https://weathernews.jp/")
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find_all("div", attrs={"class": "youtube__info"})
    link = ""
    for tag in div:
        link = tag.find('a')['href']
    await ctx.send(link)
# bot.loop.create_task(background_task())
bot.run(TOKEN)