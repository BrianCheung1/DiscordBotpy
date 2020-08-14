import discord
from discord.ext import commands
import traceback
import os
import sys
import json

#         #if the message has more than 4 e's then itll print out a message
#         if message.content.count('e') > 3 and str(message.author) not in valid_users:
#             if message.author.bot:
#                 return
#             await message.channel.send('fuck you ' + str(message.author.mention))
    
#     async def on_message_delete(self, message):
#         valid_users = ['butter#4293']
#         bad_words = ['fuck', 'gay', 'weird', 'fk', 'shit']
#         #when messages get deleted print out who deleted them
#         if message.author.bot:
#             return
#         if str(message.author) not in valid_users:
#             return
#         for word in bad_words:
#             if message.content.count(word) > 0:
#                 return
#         await message.channel.send("`" + str(message.author) + " deleted a message`")
#         await message.channel.send("What was deleted: ||" + message.content + "||")



bot = commands.Bot(command_prefix='`', case_insensitive=True)
bot.remove_command('help')

initial_extensions = ['cogs.MessageLogger', 'cogs.BotReady', 'cogs.NumOfUsers', 'cogs.ReloadCogs', 'cogs.CoinFlip', 'cogs.Roll', 'cogs.RPS', 'cogs.Blackjack', 'cogs.Help', 'cogs.Hangman', 'cogs.Profile',
'cogs.Russian', 'cogs.Server']

if __name__ == '__main__':
    #for extension in initial_extensions:
    for filename in os.listdir(f"E:/codes/Python/DiscordBotpy/cogs"):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
        # try:
        #     bot.load_extension(extension)
        # except Exception as e:
        #     print(f'Failed to load extension {extension}', file=sys.stderr)
        #     traceback.print_exc()

bot.run('NzM0OTcxNTYxODc4MDkzODQ0.XxZdwQ.IYEFR-qLIO_aJzuWkyiHwWmd5UI')