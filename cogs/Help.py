import discord
from discord.ext import commands
import asyncio

class Help(commands.Cog):
    """Prints out information about commands"""
    
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Commands", description='Information on commands', colour = ctx.author.colour)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='``balance`', value="Shows balance of user")
        embed.add_field(name='``bj [amount]`', value="Starts a game of blackjack, optional: bet amount")
        embed.add_field(name='``flip`', value="Flip a coin heads or tail")
        embed.add_field(name='``hangman`', value="starts a game of hangman")
        embed.add_field(name='``help`', value="Display this embed")
        embed.add_field(name='``profile`', value="Display information on user")
        embed.add_field(name='``users`', value="Returns number of total users, online users, offline users")
        embed.add_field(name='``roll [number]`', value="Roll a dice, default 1-6, can add a number at the end to roll 1-#")
        embed.add_field(name='``rps`', value="Play a game of rps")
        embed.add_field(name='``russian`', value="Play a game of russian roulette")
        embed.add_field(name='``stats`', value="Shows stats for hangman")
        await ctx.channel.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
    print("Help is loaded")