import discord
from discord.ext import commands
import asyncio
from aiohttp import request


class Options(commands.Cog):
    """convert alerts to look better"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def buy(self, ctx, arg1, arg2, arg3, arg4):
        await ctx.message.delete()
        embed = discord.Embed(title="Ticker: " + arg1.upper() + "-Entry",
                              description=str(ctx.author), colour=ctx.author.colour)
        embed.add_field(name="Call/Put: ", value=arg2, inline=True)
        embed.add_field(name="Expiration: ", value=arg3, inline=True)
        embed.add_field(name="Price: ", value=arg4, inline=True)
        embed.set_image(
            url=f'https://charts2.finviz.com/chart.ashx?t={arg1}&ty=c&ta=1&p=d&s=l.png')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def sell(self, ctx, arg1, arg2, arg3, arg4):
        await ctx.message.delete()
        embed = discord.Embed(title="Ticker: " + arg1.upper() + "-Exit",
                              description=str(ctx.author), colour=ctx.author.colour)
        embed.add_field(name="Call/Put: ", value=arg2, inline=True)
        embed.add_field(name="Expiration: ", value=arg3, inline=True)
        embed.add_field(name="Price: ", value=arg4, inline=True)
        embed.set_image(
            url=f'https://charts2.finviz.com/chart.ashx?t={arg1}&ty=c&ta=1&p=d&s=l.png')
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=['ct'])
    async def chart(self, ctx, arg):
        await ctx.channel.send(f'https://charts2.finviz.com/chart.ashx?t={arg}&ty=c&ta=1&p=d&s=l.png')


def setup(bot):
    bot.add_cog(Options(bot))
    print("Options is loaded")
