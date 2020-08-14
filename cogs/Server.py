import discord
from discord.ext import commands
import asyncio
from pytz import timezone


class Server(commands.Cog):
    """Prints information about server"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.online_count = 0
        self.offline_count = 0
        self.bot_count = 0
        self.text_channels = 0
        self.voice_channels = 0

    @commands.command()
    async def server(self, ctx):        
        
        usercount(self, ctx)
        channelcount(self,ctx)

        current_timezone_time = ctx.message.guild.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern'))
        new_timezone_time = current_timezone_time.astimezone(timezone('US/Eastern'))

        #await ctx.channel.send("{0.name}\n{0.region}\n{0.icon_url}\n{0.member_count}\n{0.created_at}".format(ctx.author.guild))
        embed = discord.Embed(title=str(ctx.author.guild.name) + " Server", description="Information On " + str(ctx.author.guild.name))
        embed.set_thumbnail(url=ctx.author.guild.icon_url)
        embed.add_field(name="Server Creation Date: ", value="` " + str(new_timezone_time.strftime("%A, %B %d %Y @ %H:%M:%S %p")) + " `", inline=False)
        embed.add_field(name="Region: ", value = "` " + str(ctx.author.guild.region) + " `", inline= False)
        embed.add_field(name="Total Users: ", value="` " + str(ctx.author.guild.member_count) + " `" ,inline=True)
        embed.add_field(name="Online Users ", value="` " + str(self.online_count) + " `",inline=True)
        embed.add_field(name="Offline Users ", value="` " + str(self.offline_count) + " `", inline=True)
        embed.add_field(name="Bots ", value="` " + str(self.bot_count) + " `", inline=False)
        embed.add_field(name="Categories ", value="` " + str(self.categories) + " `",inline=True)
        embed.add_field(name="Text Channels ", value="` " + str(self.text_channels) + " `",inline=True)
        embed.add_field(name="Voice Channels ", value="` " + str(self.voice_channels) + " `", inline=True)
        await ctx.channel.send(content=None, embed=embed)
        
def usercount(self,ctx):
    self.online_count = 0
    self.offline_count = 0
    self.bot_count = 0

    #loops through members to see their status
    for members in ctx.author.guild.members:
        if members.status != discord.Status.offline and not members.bot :
            self.online_count += 1
        if members.status == discord.Status.offline and not members.bot:
            self.offline_count += 1
        if members.bot:
            self.bot_count += 1

def channelcount(self,ctx):
    self.text_channels = 0
    self.voice_channels = 0
    self.categories = 0
    for x in ctx.guild.text_channels:
        self.text_channels += 1
    for x in ctx.guild.voice_channels:
        self.voice_channels += 1
    for x in ctx.guild.categories:
            self.categories += 1

def setup(bot):
    bot.add_cog(Server(bot))
    print("Server is loaded")