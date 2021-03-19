import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *arg):
        url = 'https://www.youtube.com/watch?v=YUWqe1Hi3ws'
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
        except AttributeError:
            await ctx.channel.send("Not connected to any channels")
            

def setup(bot):
    bot.add_cog(Music(bot))
    print("Music is Loaded")