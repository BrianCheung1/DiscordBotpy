import discord
from discord.ext import commands
import asyncio


class Spam(commands.Cog):
    """Spams a channel"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx, members: discord.Member = None):
        """spams a user with custom message a certain amount of times"""

        await ctx.channel.send("How many mesasges do you want sent? ")

        def check(m):
            if m.author == ctx.author:
                return m.content

        amount = await self.bot.wait_for('message', check=check)
        try:
            amount = int(amount.content)
        except ValueError:
            await ctx.channel.send("Not an Interger")
            return

        await ctx.channel.send("What mesasges do you want sent? ")
        text = await self.bot.wait_for('message', check=check)
        text = str(text.content)

        if amount > 10:
            await ctx.channel.send("Max 10 Spam")
            return
        for i in range(amount):
            user = self.bot.get_user(members.id)
            if text == None:
                await user.send('👀')
            else:
                await user.send(text)

            msg = await ctx.channel.send("Spam {}".format(members.mention))
            await msg.delete()
            await asyncio.sleep(0.5)
        if amount == 1:
            await ctx.channel.send(f"1 message of {text} was sent to {members.mention}")
        else:
            await ctx.channel.send(f"{amount} messages of {text} were sent to {members.mention}")


def setup(bot):
    bot.add_cog(Spam(bot))
    print("Spam is loaded")
