import discord
from discord.ext import commands
import asyncio

class Spam(commands.Cog):
    """spams a channel"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    def check_if_it_is_me(ctx):
        return ctx.message.author.id == 706279634672549989

    @commands.command()
    @commands.check(check_if_it_is_me)
    async def spam(self, ctx, arg = 1):
        for i in range(arg):
            await ctx.channel.send("FUCK")
            await asyncio.sleep(0.5)

def setup(bot):
    bot.add_cog(Spam(bot))
    print("Spam is loaded")
