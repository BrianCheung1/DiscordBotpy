import discord
from discord.ext import commands
import asyncio


class Spam(commands.Cog):
    """spams a channel"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx, members: discord.Member = None, arg2=None, arg1=1):
        if arg1 > 10:
            await ctx.channel.send("Max 10 Spam")
            return
        for i in range(arg1):
            msg = await ctx.channel.send("Spam {}".format(members.mention))
            await msg.delete()
            user = self.bot.get_user(members.id)
            if arg2 == None:
                await user.send('👀')
            else:
                await user.send(arg2)
            await asyncio.sleep(0.5)


def setup(bot):
    bot.add_cog(Spam(bot))
    print("Spam is loaded")
