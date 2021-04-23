import discord
from discord.ext import commands
import asyncio
import random
import requests


class BotReady(commands.Cog):
    "Prints to console when bot goes online"

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.bot.bg_task = self.bot.loop.create_task(self.my_background_task())

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.bot.user))
        channel = self.bot.get_channel(441644928750321664)
        await channel.send('Bot is running')

    async def my_background_task(self):
        await self.bot.wait_until_ready()
        btc_price = as_currency(requests.get(
            'https://api.coinbase.com/v2/prices/BTC-USD/spot').json()['data']['amount'])
        eth_price = as_currency(requests.get(
            'https://api.coinbase.com/v2/prices/ETH-USD/spot').json()['data']['amount'])
        ltc_price = as_currency(requests.get(
            'https://api.coinbase.com/v2/prices/LTC-USD/spot').json()['data']['amount'])

        listofactivities = [f'BTC: {btc_price}',
                            f'ETH: {eth_price}', f'LTC: {ltc_price}']
        while not self.bot.is_closed():
            randomactivity = random.choice(listofactivities)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(randomactivity)))
            await asyncio.sleep(10)


def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)


def setup(bot):
    bot.add_cog(BotReady(bot))
    print('BotReady is Loaded')
