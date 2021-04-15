import discord
from discord.ext import commands
import asyncio


class Mute(commands.Cog):
    """Silences users in channels"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def mute(self, ctx):
        """Mutes users in channels"""
        channel = ctx.author.voice.channel

        for x in ctx.guild.voice_channels:
            if x == channel:
                for a in x.members:
                    await a.edit(mute=True)

        await ctx.channel.send("Everyone in channel muted")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def unmute(self, ctx):
        """Unmutes users in channels"""
        channel = ctx.author.voice.channel
        for x in ctx.guild.voice_channels:
            if x == channel:
                for a in x.members:
                    await a.edit(mute=False)

        await ctx.channel.send("Everyone in channel unmuted")


def setup(bot):
    bot.add_cog(Mute(bot))
    print("Mute is loaded")
