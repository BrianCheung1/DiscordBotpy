import discord
from discord.ext import commands
import asyncio
import random

class BotReady(commands.Cog):
    "Prints to console when bot goes online"

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.bot.bg_task = self.bot.loop.create_task(self.my_background_task())

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.bot.user))

    async def my_background_task(self):
        await self.bot.wait_until_ready()
        listofactivities = ['You', 'This Server', 'Youtube', 'Onlyfans', 'Porn', 'A Movie']
        while not self.bot.is_closed():
            randomactivity = random.choice(listofactivities)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(randomactivity)))
            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(BotReady(bot))
    print('BotReady is Loaded')