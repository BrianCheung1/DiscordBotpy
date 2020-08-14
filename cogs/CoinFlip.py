import discord
from discord.ext import commands
import asyncio
import random

class CoinFlip(commands.Cog):
    """flips a coin for head or tail"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx):
        coin = ['Heads', 'Tails']
        #random choice from list provided
        random_coin = random.choice(coin)
        await ctx.channel.send(random_coin)


def setup(bot):
    bot.add_cog(CoinFlip(bot))
    print('CoinFlip is loaded')