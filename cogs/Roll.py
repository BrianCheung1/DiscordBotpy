import discord
from discord.ext import commands
import asyncio
import random


class Roll(commands.Cog):
    """Rolls a dice"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, *args):
        """Rolls a dice"""
        if not args:
            randomnumber = random.randint(1, 6)
            if (randomnumber == 1):
                await ctx.channel.send("1️⃣")
            if (randomnumber == 2):
                await ctx.channel.send("2️⃣")
            if (randomnumber == 3):
                await ctx.channel.send("3️⃣")
            if (randomnumber == 4):
                await ctx.channel.send("4️⃣")
            if (randomnumber == 5):
                await ctx.channel.send("5️⃣")
            if (randomnumber == 6):
                await ctx.channel.send("6️⃣")
        else:
            randomnumber = random.randint(1, int(*args))
            printnumber = ""
            for numbers in str(randomnumber):
                if numbers == '1':
                    printnumber += "1️⃣"
                if numbers == '2':
                    printnumber += "2️⃣"
                if numbers == '3':
                    printnumber += "3️⃣"
                if numbers == '4':
                    printnumber += "4️⃣"
                if numbers == '5':
                    printnumber += "5️⃣"
                if numbers == '6':
                    printnumber += "6️⃣"
                if numbers == '7':
                    printnumber += "7️⃣"
                if numbers == '8':
                    printnumber += "8️⃣"
                if numbers == '9':
                    printnumber += "9️⃣"
                if numbers == '0':
                    printnumber += "0️⃣"
            await ctx.channel.send(printnumber)


def setup(bot):
    bot.add_cog(Roll(bot))
    print('Roll is loaded')
