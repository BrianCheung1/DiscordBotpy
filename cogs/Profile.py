import discord
from discord.ext import commands
import asyncio
from pytz import timezone


class Profile(commands.Cog):
    """Users Profile"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.userroles = ""
        self.Hangman_stats = ""

    @commands.command(aliases=['p'])
    async def profile(self, ctx, members: discord.Member = None):
        """Sends stats about the user"""
        self.wins = 0
        self.losses = 0
        self.money_balance = 0
        changeroles(self, ctx, members)

        changestats(self, ctx, members)

        embed = sendprofile(self, ctx, members)
        await ctx.channel.send(embed=embed)


def sendprofile(self, ctx, members: discord.Member = None):
    if members == None:
        members = ctx.author
    embed = discord.Embed(title=str(members.name) + "'s Profile",
                          description="Information On " + str(members.name))
    embed.set_thumbnail(url=members.avatar_url)
    embed.add_field(name="Discord Tag: ", value="` " +
                    str(members.nick) + " `", inline=False)
    embed.add_field(name="Account Creation Date: ", value="` " + str(
        members.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")) + " `", inline=False)
    embed.add_field(name="Join Date: ", value="` " + str(
        members.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")) + " `", inline=False)
    embed.add_field(name="Roles: ", value=self.userroles, inline=False)
    embed.add_field(name="Activity: ", value="` " +
                    str(members.activity) + " `", inline=False)
    embed.add_field(name="Profile Pic: ",
                    value=members.avatar_url, inline=False)
    embed.add_field(name="Hangman Stats: ", value='` Wins: ' +
                    str(self.wins) + ' Losses: ' + str(self.losses) + ' `')
    embed.add_field(name="Balance: ", value='` $' +
                    str(self.money_balance) + ' `', inline=False)
    return embed


def changestats(self, ctx, members: discord.Member = None):
    if members == None:
        members = ctx.author
    with open('stats.txt') as f:
        for line in f:
            author = str(members.id).replace(" ", "")
            wins = line.strip().split()
            if str(wins[0]) == author:
                self.wins = int(wins[1])
                self.losses = int(wins[2])

        with open('balance.txt') as f:
            for line in f:
                author = str(members.id).replace(" ", "")
                balance = line.strip().split()
                if str(balance[0]) == author:
                    self.money_balance = int(balance[1])


def changeroles(self, ctx, members: discord.Member = None):
    if members == None:
        members = ctx.author
    self.userroles = ""
    for role in members.roles:
        self.userroles += "` "
        self.userroles += role.name
        self.userroles += " `"
    self.userroles = self.userroles.replace('@', '', 1)


def setup(bot):
    bot.add_cog(Profile(bot))
    print("Profile is Loaded")
