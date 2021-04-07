# bot.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('WEATHERBOTTOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

bot = commands.Bot(command_prefix='!@#')

@bot.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

#https://translate.google.com/translate?hl=&sl=ja&tl=en&u=https://weathernews.jp/s/solive24/timetable.html
@bot.command(name='timetable')
async def nine_nine(ctx):
    await ctx.send("It works!")

bot.run(TOKEN)