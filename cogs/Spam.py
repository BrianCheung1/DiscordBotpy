import discord
from discord.ext import commands
import asyncio


class Spam(commands.Cog):
    """spams a channel"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx, members: discord.Member = None, arg=1):
        if arg > 10:
            await ctx.channel.send("Max 10 Spam")
            return
        for i in range(arg):
            await ctx.channel.send("Spam {}".format(members.mention))
            await asyncio.sleep(0.5)


def setup(bot):
    bot.add_cog(Spam(bot))
    print("Spam is loaded")
