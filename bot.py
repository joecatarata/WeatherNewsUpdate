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

load_dotenv()
TOKEN = os.getenv('WEATHERBOTTOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

bot = commands.Bot(command_prefix='!@#')

# WHEN = time(12, 20, 00)  # 6:00 PM
# channel_id = 829325798002393129 # Put your channel id here

# async def called_once_a_day():  # Fired every day
#     await bot.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
#     channel = bot.get_channel(channel_id) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
#     await channel.send(embed=get_schedule)

# async def background_task():
#     now = datetime.utcnow()
#     print(now)
#     if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
#         tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
#         seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
#         await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
#     while True:
#         now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
#         target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
#         seconds_until_target = (target_time - now).total_seconds()
#         await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
#         await called_once_a_day()  # Call the helper function that sends the message
#         tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
#         seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
#         await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration

# target_channel_id = 829325798002393129

# @tasks.loop(hours=24)
# async def called_once_a_day():
#     message_channel = bot.get_channel(target_channel_id)
#     print(f"Got channel {message_channel}")
#     await message_channel.send(embed=get_schedule())

# @called_once_a_day.before_loop
# async def before():
#     await bot.wait_until_ready()
#     print("Finished waiting")

# called_once_a_day.start()

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
    embed = discord.Embed(title='WeatherNewsJP Schedule')
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

    
    embed.add_field(name = 'UTC+9 JPN', value= timestring, inline = True)
    embed.add_field(name = 'Title', value = titlestring, inline = True)
    embed.add_field(name = 'Newscaster', value = casterstring, inline = True)

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
