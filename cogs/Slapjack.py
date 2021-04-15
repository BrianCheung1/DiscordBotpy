import discord
from discord.ext import commands
import asyncio
import random

class Slapjack(commands.Cog):
    """Plays a game of slapjack"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
    
    @commands.command()
    async def slap(self, ctx):
        embed = discord.Embed(title="SlapJack", description='Information on commands', colour=ctx.author.colour)
        embed.add_field(name='`Number:`', value=convertcards(1))
        embed.add_field(name='`Card:`', value=convertcards(randomnumber()), inline=False)
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(1)

        i = 2
        self.cardnumber = 0

        while i <= 13:
            self.cardnumber = randomnumber()
            embed = discord.Embed(title="SlapJack", description='Information on commands', colour=ctx.author.colour)
            embed.add_field(name='`Number:`', value=convertcards(i))
            embed.add_field(name='`Card:`', value=convertcards(self.cardnumber), inline=False)

            if self.cardnumber == i:
                print(i)
                print(self.cardnumber)
                await ctx.channel.send('same')
                await self.bot.wait_for('message', check=check, timeout=30)

            def check(message):
                return message.content == 'slap'
                
            await msg.edit(embed=embed)
            await asyncio.sleep(1)
            i += 1

        
        await ctx.channel.send('Done')


def randomnumber():
    listofcards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    randomcard = random.choice(listofcards)
    return randomcard

def convertcards(card):
    randomtencard = [':keycap_ten:',':regional_indicator_j:', ':regional_indicator_q:', ':regional_indicator_k:']
    if card == 1:
        card = ':a:'
    if card == 2:
        card = '2️⃣'
    if card == 3:
        card = '3️⃣'
    if card == 4:
        card = '4️⃣'
    if card == 5:
        card = '5️⃣'
    if card == 6:
        card = '6️⃣'
    if card == 7:
        card = '7️⃣'
    if card == 8:
        card = '8️⃣'
    if card == 9:
        card = '9️⃣'
    if card == 10:
        card = ':keycap_ten:'
    if card == 11:
        card = ':regional_indicator_j:'
    if card == 12:
        card = ':regional_indicator_q:'
    if card == 13:
        card = ':regional_indicator_k:'
    return card


def setup(bot):
    bot.add_cog(Slapjack(bot))
    print("Slapjack is loaded")