# Standard python libraries
import os
import json

# External Imports
from discord.ext import commands, tasks
from dotenv import load_dotenv
import aiocron

# Internal Project Imports
from ctftime import get_ctfs_this_week

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
ALERT_TIME = '00 08 * * 1'  # in cron format

bot = commands.Bot(command_prefix='!')

def create_ctf_message(ctf: dict):
    def parse_time(time_: str):
        date = time_.split('T')[0]
        time_ = time_.split('T')[1].split('+')[0]
        return f'{date} {time_} UTC' 

    return (
        '>>> ' + '**Title:**\t' + ctf['title'] + '\n'
        '**Description:** \n' + ctf['description'][0:200] + '...' + '\n'
        '**URL**: ' + '<' + ctf['url'] + '>' + '\n'
        '**Ctftime URL:**\t' + '<' + ctf['ctftime_url'] + '>' + '\n'
        '**Start:**\t' + parse_time(ctf['start']) + '\n'
        '**Finish:**\t' + parse_time(ctf['finish']) + '\n'
        )

@bot.event
async def on_ready():
    # Gets the guild ID
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    await connection_output(bot, guild)
    # Gets the channel
    alert_channel = await bot.fetch_channel(CHANNEL_ID)
    print(f'Ready to message on {alert_channel.name}')

# Commands
@bot.command(name="ctfs_week")
async def this_weeks_ctfs(ctx):
    ctfs_response = get_ctfs_this_week()
    ctfs = ctfs_response.json()
    response = f"This week's ctfs are:\n"
    await ctx.send(response)
    for ctf in ctfs:
        ctf_message = create_ctf_message(ctf)
        await ctx.send(ctf_message)

# Cron
@aiocron.crontab(ALERT_TIME)
async def send_weeks_ctfs():
    alert_channel = await bot.fetch_channel(CHANNEL_ID)
    ctfs_response = get_ctfs_this_week()
    ctfs = ctfs_response.json()
    response = f"This week's ctfs are:\n"
    await alert_channel.send(response)
    for ctf in ctfs:
        ctf_message = create_ctf_message(ctf)
        await alert_channel.send(ctf_message)

async def connection_output(discord_bot: object, discord_guild: object):
    print(f'{discord_bot.user.name} connected to {discord_guild.name}')

async def test_message(channel: object, message="Testing 1.. 2.. 3.."):
    """
    >>> alert_channel = await bot.fetch_channel(CHANNEL_ID)
    >>> await test_message(alert_channel)
    """
    print("Sending test message:")
    print(f"  {message}")
    await channel.send(message)

bot.run(TOKEN)