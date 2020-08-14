import discord
from discord.ext import commands
import asyncio

class Mute(commands.Cog):
    """Mute a person in a server"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot


    @commands.command()
    async def mute(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return
        channel = ctx.author.voice.channel

        for x in ctx.guild.voice_channels:
            if x == channel:
                for a in x.members:
                    await a.edit(mute=True)
                    await asyncio.sleep(0.5)

        await ctx.channel.send("Everyone in channel muted")

    @commands.command()
    async def unmute(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return

        channel = ctx.author.voice.channel
        for x in ctx.guild.voice_channels:
            if x == channel:
                for a in x.members:
                    await a.edit(mute=False)
                    await asyncio.sleep(0.5)

        await ctx.channel.send("Everyone in channel unmuted")


def setup(bot):
    bot.add_cog(Mute(bot))
    print("Mute is loaded")
