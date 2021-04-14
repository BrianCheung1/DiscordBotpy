import discord
from discord.ext import commands
import asyncio
import random


class RPS(commands.Cog):
    """Play rock paper scissors"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, arg):

        rps = ['✊', '🖐️', '✌️']
        randomrps = random.choice(rps)

        if arg.lower() == 'rock':
            arg = '✊'
        if arg.lower() == 'scissors' or arg.lower() == 'scissor':
            arg = '✌️'
        if arg.lower() == 'paper':
            arg = '🖐️'

        await ctx.channel.send(ctx.author.mention + ' picked ' + arg)
        await ctx.channel.send('Bot picked ' + str(randomrps))

        if arg == '✊':
            if str(randomrps) == '✊':
                await ctx.channel.send('Tie')
            if str(randomrps) == '✌️':
                await ctx.channel.send('You Win')
            if str(randomrps) == '🖐️':
                await ctx.channel.send('You Lose')
        if arg == '✌️':
            if str(randomrps) == '✊':
                await ctx.channel.send('You Lose')
            if str(randomrps) == '✌️':
                await ctx.channel.send('Tie')
            if str(randomrps) == '🖐️':
                await ctx.channel.send('You Win')
        if arg == '🖐️':
            if str(randomrps) == '✊':
                await ctx.channel.send('You Win')
            if str(randomrps) == '✌️':
                await ctx.channel.send('You Lose')
            if str(randomrps) == '🖐️':
                await ctx.channel.send('Tie')


def to_lower(arguments):
    return arguments.lower()


def setup(bot):
    bot.add_cog(RPS(bot))
    print('RPS is loaded')
