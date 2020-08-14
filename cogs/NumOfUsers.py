import discord
from discord.ext import commands
import asyncio

class NumOfUsers(commands.Cog):
    "Prints total number of users, online users, offline users"

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def users(self, ctx):
        id = self.bot.get_guild(152954629993398272)
        channels = ["music-spam-etc"]

        if str(ctx.channel) in channels:
            await ctx.channel.send('# of members: `' + str(id.member_count) + '`')
            online_count = 0
            offline_count = 0
            #loops through members to see their status
            for members in id.members:
                if members.status != discord.Status.offline:
                    online_count += 1
                if members.status == discord.Status.offline:
                    offline_count += 1
            await ctx.channel.send('# of online members: `' + str(online_count) + '`')
            await ctx.channel.send('# of offline members: `' + str(offline_count) + '`')
def setup(bot):
    bot.add_cog(NumOfUsers(bot))
    print('NumOfUsers is Loaded')