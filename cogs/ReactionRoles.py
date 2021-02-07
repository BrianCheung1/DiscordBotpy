import discord
from discord.ext import commands
import asyncio
from discord.utils import get


class ReactionRoles(commands.Cog):
    """Prints out information about commands"""
    
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
    
    @commands.command(aliases = ['rr'])
    async def reaction(self,ctx):
        await ctx.channel.send("Enter message you would like to have reaction added to")
        msg = await self.bot.wait_for('message')
        await msg.add_reaction('👍')
        await ctx.channel.send("Enter role you like users to recieve")
        role = await self.bot.wait_for('message')
        await ctx.author.add_roles(role.content)
        

    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     if user.bot:
    #         return

    #     channel = reaction.message.channel
    #     await channel.send(str(user.mention) + " has been given the role ...")
    #     await channel.send("fuck ricky")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))
    print("Reaction Roles is loaded")