import discord
from discord.ext import commands
import asyncio
import traceback
import os
import sys
import json

class ReloadCogs(commands.Cog):
    "Reloads cogs if changes are made"

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot


    @commands.command()
    #reloads all the extensions in the list
    async def reload(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return

        for filename in os.listdir(f"C:/Codes/Python/DiscordBotpy/cogs"):
            if filename.endswith('.py'):
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
        await ctx.channel.send('Cogs Reloaded')

    @commands.command()
    #loads extensions manually 
    async def load(self, ctx ,extension):
        try:
            self.bot.load_extension(f'cogs.{extension}')
            await ctx.channel.send('{} Loaded'.format(extension))
            print('Loaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
    
    @commands.command()
    #unloads extensions manually 
    async def unload(self,ctx,extension):
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            await ctx.channel.send('{} unloaded'.format(extension))
            print('Unloaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be unloaded. [{}]'.format(extension, error))

def setup(bot):
    bot.add_cog(ReloadCogs(bot))
    print('ReloadCogs is Loaded')