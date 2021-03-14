import discord
from discord.ext import commands
import traceback
import os
import sys
import json

with open('./config.json', 'r') as cjson:
    config = json.load(cjson)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or('`'), intents=intents, case_insensitive=True)
bot.remove_command('help')

if __name__ == '__main__':
    # for extension in initial_extensions:
    for filename in os.listdir(f"./cogs"):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(config['token'])
