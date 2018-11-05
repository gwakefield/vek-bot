import os
import discord
import asyncio
import logging
import random
import sys
import time

from constants import *
from datetime import date, datetime, timedelta
from discord.ext import commands
from threading import Thread

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

TOKEN = os.environ.get('TOKEN')
ENABLE_TASK = True
BODILY_SECONDS = 33084 # easter egg!

bot = commands.Bot(command_prefix='!', description='A Vekker bot for the Vekilites')

def heardYouCorrectly():
    return random.random() > 0.2

def getGroupMembers(group):
    members = []
    allMembers = bot.get_all_members()
    for member in allMembers:
        if group in (r.name for r in member.roles):
            members.append(member)
    return members

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Game(name=random.choice(VEK_STATUSES)))

@bot.event
async def on_message(message): 
    if(message.author.name == 'livewire90210'):
        if("to be fair" in message.content.lower() or "tbf" in message.content.lower()):
            await message.channel.send("TO BE FAIR!....")
    if(message.author.name == 'mleeneg'):
        parts = message.content.lower().split(' ')
        swore = [a in SWEAR_FILTER for a in parts]
        if(TRUE in swore):
            await message.channel.send("Meng swore!!!")

@bot.command()
async def hello(ctx):
    if heardYouCorrectly():
        await ctx.send('*creepy smile*')
    else:
        await ctx.send(f'{ctx.message.author.name}, did you say you want some jello?')

@bot.command()
async def vek(ctx):
    if heardYouCorrectly():
        await ctx.send('Kevin for President!')
    else:
        await ctx.send('Me kiiiiiitty~!')

@bot.command()
async def directions(ctx):
    if heardYouCorrectly():
        await ctx.send(random.choice(VEK_DIRECTIONS))
    else:
        await ctx.send('Did you say dull erections??')

@bot.command()
async def favoriteband(ctx):
    if heardYouCorrectly():
        await ctx.send('Led Zepplin. The greatest band of all time.')
    else:
        await ctx.send('Did you just say favorite man? That\'d be ' + random.choice(VEK_TARGETS))

@bot.command()
async def config(ctx):
    global ENABLE_TASK, BODILY_SECONDS

    parts = ctx.message.content.split(' ')
    if len(parts) < 3:
        embed = discord.Embed(title="Vekker Bot Config", description="List of configurations are:", color=0xeee657)

        embed.add_field(name="!config tasks on|off", value="Enable or disable background tasks", inline=False)
        embed.add_field(name="!config bodily <seconds>", value="Set the number of seconds between Vek bodily functions", inline=False)

        await ctx.send(embed=embed)
    else:
        setting = parts[1].lower()
        value = parts[2]

        if setting != "tasks":
            try:
                value = int(parts[2])
            except ValueError:
                await ctx.send(f'!config {parts[1]} <value> must be an number')
                return

        if setting == 'tasks':
            ENABLE_TASK = value == 'enable' or value == 'on' or value == 'true'
        if setting == 'bodily':
            BODILY_SECONDS = value
        await ctx.send(f'**config.{parts[1]}** set to {parts[2]}')

@bot.command()
async def info(ctx):
        embed = discord.Embed(title="Vekker Bot", description="To get your daily weird fix", color=0xeee657)

        # give info about you here
        embed.add_field(name="Author", value="rngeoff")

        # Shows the number of servers the bot is member of.
        embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

        # Shows link to GitHub code
        embed.add_field(name="GitHub", value="https://github.com/")

        await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Vekker Bot", description="MOAR Vek!! List of commands are:", color=0xeee657)

    embed.add_field(name="!hello", value="Say hi to vek-bot", inline=False)
    embed.add_field(name="!vek", value="A vote of confidence for Kevin", inline=False)
    embed.add_field(name="!directions", value="Ask Kevin for directions", inline=False)
    embed.add_field(name="!info", value="Details on the bot that is Kevin", inline=False)
    embed.add_field(name="!config", value="See instructions on configurating settings", inline=False)

    await ctx.send(embed=embed)

async def idle_task():
    await bot.wait_until_ready()

    channel = discord.utils.get(bot.get_all_channels(), name='upisdown')

    last_bodily_dt = datetime.now()

    while not bot.is_closed():
        now = datetime.now()

        # if config enabled and not while we're sleeping
        if not ENABLE_TASK or now.hour < 8:
            continue

        # bodily functions
        delta = now - last_bodily_dt
        if delta.seconds > BODILY_SECONDS:
            last_bodily_dt = datetime.now()
            await channel.send(f'{random.choice(VEK_BODILY_FUNCTIONS)}')

        await asyncio.sleep(15) # task runs every 15 seconds
    print('idle_task() exit')

# Run watcher
bot.loop.create_task(idle_task())
# Run bot
bot.run(TOKEN)
