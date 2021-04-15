import discord
from discord.ext import commands
import asyncio
import re
from pytz import timezone
from datetime import datetime

class MessageLogger(commands.Cog):
    """Logs Messsage sent in server"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        bad_words = ['fuck', 'gay', 'fk', 'shit', 'fuq', 'fuk']
        #current_timezone_time = ctx.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern'))
        #new_timezone_time = current_timezone_time.astimezone(timezone('US/Eastern'))
        now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

        #logs messages from users of the guild to console
        print('[{}] '.format(dt_string) + 'Message from {0.author} in "{0.channel}": {0.content}'.format(ctx))
        #if the author of a message is a bot stop
        if ctx.author.bot:
            return
        #in list of bad words, if it is seen purge it
        # for words in bad_words:
        #     if remove(ctx.content.lower()).count(words) > 0 and str(ctx.author) not in listvalidusers():
        #         print(ctx.content)
        #         await ctx.channel.purge(limit=1)
        #         await ctx.channel.send("```" + str(ctx.author) + " said a bad word```")
        #         await ctx.channel.send("What they said: ||" + ctx.content + "||") 
        #         await ctx.channel.send("That was mean")

        #if message contains 3 or more e's, censor it
        # if (ctx.content.lower().count('e')) >= 3 and str(ctx.author) not in listvalidusers() and ctx.content.lower().find('https') < 0:
        #     await ctx.channel.purge(limit=1)
        #     await ctx.channel.send('Message by ' + ctx.author + ' Got Censored. Message Censored: `' + ctx.content + '`')
        #await self.bot.process_commands(ctx)

    # @commands.command()
    # async def role(self, ctx, arg=None):
    #     self.players = []
    #     self.player_list = ""
    #     self.message_id = ""
    #     self.role_message = await ctx.channel.send('Click to receive role ' + arg)
    #     await self.role_message.add_reaction('✅')
    #     self.message_id = self.role_message.id

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        channel = reaction.message.channel
        id = reaction.message.id
        if self.message_id != id:
            return
        if user.bot:
            return
        for i in range(0, len(self.players)):
            if self.players[i] == user.mention:
                return
        self.players.append(user.mention)

        self.player_list += str(user.mention) + " "

        await self.role_message.edit(content=str(self.role_message.content) + "\n " + self.player_list)

        for member in self.role_message.guild.members:
            await member.add_roles(roles = '741033092092788878')

#returns list of valid users
def listvalidusers():
    valid_users = ['butter#4293']
    return valid_users

def remove(string):
    whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return ''.join(filter(whitelist.__contains__, string))

def setup(bot):
    bot.add_cog(MessageLogger(bot))
    print('MessageLogger is loaded')

