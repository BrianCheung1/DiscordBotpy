import discord
from discord.ext import commands
import asyncio
import random

class Russian(commands.Cog):
    """Plays a game of Russian Roulette"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.game_started = False
        self.players = []
        self.message_id = ""
        self.player_list = ""
    
    @commands.command()
    async def russian(self, ctx, members: discord.Member=None):
        self.players = []
        self.message_id = ""
        self.player_list = ""
        self.game_started = True
        self.start_message = await ctx.channel.send('Click the Check emoji to join')
        await self.start_message.add_reaction('✅')
        await ctx.channel.send('`start to start game')
        self.message_id = self.start_message.id

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        id = reaction.message.id
        if self.message_id != id:
            return
        if user.bot:
            return
        if self.game_started == False:
            return
        
        for i in range(0, len(self.players)):
            if self.players[i] == user.mention:
                return
        self.players.append(user.mention)

        self.player_list += str(user.mention) + " "

        await self.start_message.edit(content='Click the Check emoji to join\n {} is playing '.format(str(self.player_list)))

    @commands.command()
    async def start(self, ctx):
        if self.game_started == False:
            await ctx.channel.send('No games in process')
            return
        if len(self.players) <= 1:
            await ctx.channel.send('Need at least two players to start a game')
            return
        for i in range(0, len(self.players) - 1):
            list_of_deaths = [
                'Was shot in the face by an intruder.'
                ,'Drowned in the ocean.'
                ,'Was unable to breathe (emphysema or heart failure).'
                ,'Trapped in a car that fell off a bridge.'
                ,'Was crushed by a stampeding mob.'
                ,'Had radiation poisoning (Too much toxicity).'
                ,'Got bit by a rabid animal (foaming at the mouth, convulsing uncontrollably, etc.).'
                ,'Had anaphylaxis from a bee bite or from drugs (a variation on not being able to breathe).'
                ,'Got Poisoned from contaminated vegetables or chicken that has not been handled properly.'
                ,'Ended up with alzheimer’s disease (not being able to remember family, not being able to talk).'
                ,'Lost to brain tumors (uncontrollable headaches, convulsions, operations, pain).'
                ,'Got AIDS (slow wasting away, an embarrassing disease, prolonged course).'
                ,'Had multiple sclerosis (losing bodily functions, one after the other, crippled, blind, prolonged course).'
                ,'Has diabetes (amputations, blindness, untreatable ulcers, kidney dialysis).'
                ,'Died to a complication of surgery (going to sleep and expecting to wake up, but not waking up).'
                ,'Died to a pointless, sudden accident, such as getting hit by a bus that jumps the curb.'
                ,'Had gastrointestinal diseases that cause incontinence, or other such deaths that are undignified and embarrassing.'
            ]
            randomplayer = random.choice(self.players)
            await ctx.channel.send(randomplayer + str(random.choice(list_of_deaths)))
            self.players.remove(randomplayer)
            await ctx.channel.send('Choosing next player to die...')
            await asyncio.sleep(3)
            

        self.player_list = self.players[0]
        await ctx.channel.send(str(self.player_list) + " lived to play another game")
        self.game_started = False

def setup(bot):
    bot.add_cog(Russian(bot))
    print('Russian is loaded')