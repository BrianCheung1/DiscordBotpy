import discord
from discord.ext import commands
import asyncio
import random

class Slot(commands.Cog):
    """Plays the slot machine"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot


    @commands.command()
    async def slot(self, ctx):
        machine = ['7️⃣', '🍋', '🍒', '❤️', '🍎']
        lines = ""
        for i in range(3):
            lines += str(random.choice(machine)) + str(random.choice(machine)) + str(random.choice(machine)) + "\n"
        embed = discord.Embed(title="Slot machine", description=lines, colour=ctx.author.colour)
        await ctx.channel.send(embed=embed)
        msg = await ctx.channel.send("Spin Again?")
        await msg.add_reaction('✅',)
        await msg.add_reaction('⛔')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        


def setup(bot):
    bot.add_cog(Slot(bot))
    print("Slot is loaded")