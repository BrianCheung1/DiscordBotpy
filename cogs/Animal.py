import discord
from discord.ext import commands
import asyncio
import random
import os
from aiohttp import request
from dotenv import load_dotenv

load_dotenv()
x_rapidapi_host = os.getenv("x-rapidapi-host")
x_rapidapi_key = os.getenv("x-rapidapi-key")
Authorization = os.getenv("Authorization")


class Animal(commands.Cog):
    """Prints Random Animal Fact"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def dog(self, ctx):
        URL = "https://some-random-api.ml/facts/dog"
        image = "https://some-random-api.ml/img/dog"

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                await ctx.send(f'`{data["fact"]}`')
            else:
                await ctx.send(f"API returned a {response.status} status.")

        async with request("GET", image, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                await ctx.send(data["link"])
            else:
                image = None

    @commands.command()
    async def urban(self, ctx, arg=None):
        if arg == None:
            await ctx.send('provide something to search')
            return

        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        querystring = {"term": arg}

        headers = {
            'x-rapidapi-host': x_rapidapi_host,
            'x-rapidapi-key': x_rapidapi_key
        }

        async with request("GET", url, headers=headers, params=querystring) as response:
            if response.status == 200:
                data = await response.json()
                await ctx.send(f'Defintion:  {data["list"][0]["definition"]}')
                await ctx.send(f'Thumbsup: {data["list"][0]["thumbs_up"]}')
                await ctx.send(f'Thumbsdown: {data["list"][0]["thumbs_down"]}')
                await ctx.send(f'Link: {data["list"][0]["permalink"]}')

    @commands.command()
    async def twitter(self, ctx, arg=None):
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=NobodySpecialO&count=2'
        headers = {'Authorization': Authorization}

        querystring = {}
        async with request("GET", url, headers=headers, params=querystring) as response:
            if response.status == 200:
                data = await response.json()
                print(data[0].keys())
                await ctx.send(data[0]['created_at'])
                await ctx.send(data[0]['text'])
                await ctx.send(data[1]['created_at'])
                await ctx.send(data[1]['text'])


def setup(bot):
    bot.add_cog(Animal(bot))
    print("Animal is loaded")
