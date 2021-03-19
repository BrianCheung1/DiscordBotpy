import discord
from discord.ext import commands

class Math(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def math(self, ctx, *, arg=None):
        if arg is None:
            await ctx.channel.send("No Arguments Provided")
        else:
            if '+' in arg:
                arg = arg.split('+')
                await ctx.channel.send(float(arg[0]) + float(arg[1]))
            elif '-' in arg:
                arg = arg.split('-')
                await ctx.channel.send(float(arg[0]) - float(arg[1]))
            elif 'x' in arg:
                arg = arg.split('x')
                await ctx.channel.send(float(arg[0]) * float(arg[1]))
            elif '*' in arg:
                arg = arg.split('*')
                await ctx.channel.send(float(arg[0]) * float(arg[1]))
            elif '/' in arg:
                arg = arg.split('/')
                await ctx.channel.send(float(arg[0]) / float(arg[1]))    

def setup(bot):
    bot.add_cog(Math(bot))
    print("Math is Loaded")