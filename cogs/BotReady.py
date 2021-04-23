import discord
from discord.ext import commands
import asyncio
import random
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv

load_dotenv()
CMC_PRO_API_KEY = os.getenv("X-CMC_PRO_API_KEY")


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

        while not self.bot.is_closed():
        btc_price = as_currency(float(requests.get(
            'https://api.coinbase.com/v2/prices/BTC-USD/spot').json()['data']['amount']))
        eth_price = as_currency(float(requests.get(
            'https://api.coinbase.com/v2/prices/ETH-USD/spot').json()['data']['amount']))
        ltc_price = as_currency(float(requests.get(
            'https://api.coinbase.com/v2/prices/LTC-USD/spot').json()['data']['amount']))

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=DOGE,SAFEMOON&convert=USD'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': CMC_PRO_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url)
            data = json.loads(response.text)
            doge_price = as_currency(
                data['data']['DOGE']['quote']['USD']['price'])
            safemoon_price = float(
                data['data']['SAFEMOON']['quote']['USD']['price'])
            safemoon_price = '{:,.8f}'.format(safemoon_price)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        listofactivities = [f'BTC at {btc_price}',
                            f'ETH at {eth_price}', f'LTC at {ltc_price}', f'DOGE at {doge_price}', f'SAFEMOON at ${safemoon_price}']
        for item in listofactivities:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=item))
            await asyncio.sleep(30)


def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)


def setup(bot):
    bot.add_cog(BotReady(bot))
    print('BotReady is Loaded')
