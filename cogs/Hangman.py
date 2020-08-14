import discord
from discord.ext import commands
import asyncio
import logging
import random

class Hangman(commands.Cog):
    """starts a game of hangman"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.chosen_word = ""
        self.guessed_letters = ""
        self.used_letters = []
        self.remaining_guesses = 6
        self.words = []
        with open('words.txt') as f:
                for line in f:
                    word = line.strip()
                    self.words.append(word)
    
        self.has_ended = False
        self.has_won = False
        self.player = None
        self.game_started = False
        self.user = ""
        self.own_word = False
        self.dictionaries = {}
        self.wins = 0
        self.losses = 0
        self.players = []
        self.check_message = ""

 
    @commands.command(aliases=['hang'])
    #starts a game of hangman
    async def hangman(self, ctx):
        self.wins = 0
        self.losses = 0
        self.is_player = True

        #opens file and sets wins and losses to their respective players
        with open('stats.txt') as f:
            author = str(ctx.author.id).replace(" ", "") 
            if author not in f.read():
                self.is_player = False
        
        if self.is_player == True:
            with open('stats.txt') as f:
                for line in f:
                    wins = line.strip().split()
                    author = str(ctx.author.id).replace(" ", "") 
                    if str(wins[0]) == author:
                        self.wins = int(wins[1])
                        self.losses = int(wins[2])

        #creates a new line if player has never played
        if self.is_player == False:
            f = open('stats.txt', 'a')
            self.wins = 0
            self.losses = 0
            author = str(ctx.author.id).replace(" ", "")
            f.write(author + " " + str(self.wins) + " " + str(self.losses) + "\n")
            f.close()

        #if player started and game and started again before ending
        #they go up by 1 loss
        if ctx.author.id in self.dictionaries:
            if self.dictionaries[ctx.author.id]["self.game_started"] == True:
                self.losses += 1

                reading_file = open("stats.txt", "r")
                new_file_content = ""

                for line in reading_file:
                    stripped_line = line.strip()
                    wins = stripped_line.split()
                    author = str(ctx.author.id).replace(" ", "") 
                    if str(wins[0]) == author:
                        wins[2] = str(self.losses)
                        new_line = ' '.join(wins)
                        new_file_content += new_line + "\n"
                    else:
                        new_line = stripped_line
                        new_file_content += new_line + "\n"
                reading_file.close()

                writing_file = open("stats.txt", "w")
                writing_file.write(new_file_content)
                writing_file.close()

        
        #if the player has not played before, set their values
        if ctx.author.id not in self.dictionaries:
            self.dictionaries[ctx.author.id] = {
            "self.player": ctx.author.id,
            "self.chosen_word" : "",
            "self.guessed_letters" : "",
            "self.remaining_guesses" : 6,
            "self.has_ended" : False,
            "self.has_won" : False,
            "self.used_letters" : [],
            "self.own_word" : False,
            "self.user": "",
            "self.edit_word": "",
            "self.msg": "",
            "self.game_started" : False
            }

        #if the player has played before, reset their values
        if ctx.author.id in self.dictionaries:
            self.dictionaries[ctx.author.id]['self.player'] = ctx.author.id
            self.dictionaries[ctx.author.id]["self.remaining_guesses"] = 6
            self.dictionaries[ctx.author.id]["self.chosen_word"] = ""
            self.dictionaries[ctx.author.id]["self.guessed_letters"] = ""
            self.dictionaries[ctx.author.id]["self.has_ended"] = False
            self.dictionaries[ctx.author.id]["self.has_won"] = False
            self.dictionaries[ctx.author.id]["self.used_letters"] = []
            self.dictionaries[ctx.author.id]["self.own_word"] = False
            self.dictionaries[ctx.author.id]["self.user"] = ""
            self.dictionaries[ctx.author.id]["self.edit_word"] = ""
            self.dictionaries[ctx.author.id]["self.msg"] = ""
            self.dictionaries[ctx.author.id]["self.game_started"] = False

        #wait for user choice of random word or their own word
        await ctx.channel.send("Type `random` for random word, or type `own` to start a game with your own words for others to guess")

        def check(m):
            return m.content

        #set msg to user input
        self.dictionaries[ctx.author.id]["self.msg"] = await self.bot.wait_for('message', check=check)

        print(check(self.dictionaries[ctx.author.id]["self.msg"]))
        #if user input is not random/own or another user typed wait for message
        while (self.dictionaries[ctx.author.id]["self.msg"].author.id != ctx.author.id or check(self.dictionaries[ctx.author.id]["self.msg"]) != 'random' and check(self.dictionaries[ctx.author.id]["self.msg"]) !='own'):
            self.dictionaries[ctx.author.id]["self.msg"] = await self.bot.wait_for('message', check=check)

        #if message is random start random word
        if check(self.dictionaries[ctx.author.id]["self.msg"]).lower() == 'random':
            await ctx.channel.send('Random word chosen')
            self.dictionaries[ctx.author.id]["self.game_started"] = True

        #if message is own then dm user
        elif check(self.dictionaries[ctx.author.id]["self.msg"]).lower() == 'own':
            self.has_ended = False
            self.has_won = False
            self.player = None
            self.user = ""
            self.own_word = False
            self.chosen_word = ""
            self.guessed_letters = ""
            self.used_letters = []
            self.remaining_guesses = 6

            await ctx.channel.send("Check DMs")
            self.dictionaries[ctx.author.id]['self.own_word'] = True
        
        #to check message later to see if other players can guess
        self.check_message = check(self.dictionaries[ctx.author.id]["self.msg"])

        #if own word was chosen, dms the user and waits for their message
        #replaces that word with _ to hide the word
        if self.dictionaries[ctx.author.id]['self.own_word'] == True:
            self.user = self.bot.get_user(ctx.author.id)
            await self.user.send('Please provide word you want to use')
            await asyncio.sleep(1)
            self.user_response = await self.bot.wait_for('message')
            key = self.user_response.content
            self.chosen_word = key

            new_string = ""
            for i in range(0, len(self.chosen_word)):
                if self.chosen_word[i] == " ":
                    new_string += " "
                else:
                    new_string += "_"
            #sets guessed letter to new string
            self.guessed_letters = new_string

            await ctx.channel.send("Everyone can guess unless you're in a game")

            #send to channel number of guesses and letters in the word`reload
            self.edit_word = await ctx.channel.send(remainingletters(self,ctx))

        #if own word was not chosen, chose random word from word list
        if self.dictionaries[ctx.author.id]['self.own_word'] == False:
            key = random.choice(self.words)
            self.dictionaries[ctx.author.id]['self.chosen_word'] = key
            print(self.dictionaries[ctx.author.id]['self.chosen_word'])

            #sets new string to _ to represents number of letters in chosen word
            new_string = ""
            for i in range(0, len(self.dictionaries[ctx.author.id]['self.chosen_word'])):
                if self.dictionaries[ctx.author.id]['self.chosen_word'][i] == " ":
                    new_string += " "
                else:
                    new_string += "_"
            #sets the letters to the new string
            self.dictionaries[ctx.author.id]['self.guessed_letters'] = new_string

            #send to channel number of guesses and letters in the word
            self.dictionaries[ctx.author.id]['self.edit_word'] = await ctx.channel.send(remainingletters(self,ctx))

        #sends a clean embed to explain the rules of the game
        embed = discord.Embed(title="Rules", description='Information on Hangman')
        embed.set_thumbnail(url = ctx.author.avatar_url)
        embed.add_field(name='`guess ***letter***', value="Provide a letter to play")
        embed.add_field(name='`guess ***word***', value="Provide whole word to solve", inline= False)
        await ctx.channel.send(content=None, embed=embed)

    

    @commands.command(aliases=['g'])
    #allows player to guess letters in the chosen word
    async def guess(self, ctx, *, arg=None):
        #if the player thats guesses is not in dictionary it means they aren't playing their own game. 
        #creates a dict for them and sets their own word to true to allow them to guess another players word
        if arg == None:
            return
        if ctx.author.id not in self.dictionaries:
            self.dictionaries[ctx.author.id] = {
            "self.game_started" : False,
            "self.own_word" : True,
            }
        if self.check_message != 'own' and self.check_message != 'random':
            await ctx.channel.send("`hangman to start a new game")
            return

        #if player has own word set then start this condition
        if self.dictionaries[ctx.author.id]['self.own_word'] == True and self.check_message == 'own':
            #if game has already ended, reset
            if self.has_ended:
                await ctx.channel.send("`hangman to start a new game")
                return
            #if length of args are greater than 1 and is the correct word, game ends and player wins
            if len(arg) > 1:
                if arg.lower() == self.chosen_word.lower():
                    self.has_ended = True
                    self.has_won = True
                    await self.dictionaries[ctx.author.id]['self.edit_word'].edit(content=remainingletters(self, ctx))
            
            guess = ""
            guess += arg.lower()
            contains_guess = False

            #if player already used the letter provided, they have to choose another one
            for i in range(0, len(self.used_letters)):
                if guess == self.used_letters[i].lower():
                    await ctx.channel.send("Letter already used")
                    return

            #add previous letters into a string
            self.used_letters += [guess]

            #checks to see if the letter guessed is in the chosen word
            #if it is, replaces the _ with the letter
            #if it isn't remove 1 remaining_guesses
            for i in range(0, len(self.chosen_word)):
                if guess == self.chosen_word[i].lower():
                    self.guessed_letters = self.guessed_letters[:i] + self.chosen_word[i] + self.guessed_letters[i + 1:]
                    contains_guess = True
            if not contains_guess:
                self.remaining_guesses -= 1
                
            unguessed_letters = False

            #win condintions
            for letter in self.guessed_letters:
                if letter == "_":
                    unguessed_letters = True

            #if there are no more _ then player has won and game has ended
            if not unguessed_letters:
                self.has_ended = True
                self.has_won = True
                self.game_started = False
            
            #if there are no more remaining guess, player loses and game has ended
            if self.remaining_guesses < 1:
                self.has_ended = True
                self.has_won = False
                self.game_started = False

            #status of the game
            #edits the original message 
            #much cleaner than spamming the channel
            await self.edit_word.edit(content=remainingletters(self, ctx))
 
        #if player is doing random word
        elif self.dictionaries[ctx.author.id]['self.own_word'] == False and self.check_message == 'random':
            #conditions to stop the player from overguessing
            if self.dictionaries[ctx.author.id]['self.has_ended']:
                await ctx.channel.send("`hangman to start a new game")
                return
            #stop players from guessing if not their game
            if self.dictionaries[ctx.author.id]["self.player"] != ctx.author.id:
                await ctx.channel.send("You haven't started a game")
                return
            #if length of args are greater than 1 and is the correct word, game ends and player wins
            if len(arg) > 1:
                if arg.lower() == self.dictionaries[ctx.author.id]['self.chosen_word'].lower():
                    self.dictionaries[ctx.author.id]['self.has_ended'] = True
                    self.dictionaries[ctx.author.id]['self.has_won'] = True
                    await self.dictionaries[ctx.author.id]['self.edit_word'].edit(content=remainingletters(self, ctx))
                    return
            
            guess = ""
            guess += arg.lower()
            contains_guess = False

            #if player already used the letter provided, they have to choose another one
            for i in range(0, len(self.dictionaries[ctx.author.id]['self.used_letters'])):
                if guess == self.dictionaries[ctx.author.id]['self.used_letters'][i].lower():
                    await ctx.channel.send("Letter already used")
                    return

            #add previous letters into a string
            self.dictionaries[ctx.author.id]['self.used_letters'] += [guess]

            #checks to see if the letter guessed is in the chosen word
            #if it is, replaces the _ with the letter
            #if it isn't remove 1 remaining_guesses
            for i in range(0, len(self.dictionaries[ctx.author.id]['self.chosen_word'])):
                if guess == self.dictionaries[ctx.author.id]['self.chosen_word'][i].lower():
                    self.dictionaries[ctx.author.id]['self.guessed_letters'] = self.dictionaries[ctx.author.id]['self.guessed_letters'][:i] + self.dictionaries[ctx.author.id]['self.chosen_word'][i] + self.dictionaries[ctx.author.id]['self.guessed_letters'][i + 1:]
                    contains_guess = True
            if not contains_guess:
                self.dictionaries[ctx.author.id]['self.remaining_guesses'] -= 1
                
            unguessed_letters = False

            #win condintions
            for letter in self.dictionaries[ctx.author.id]['self.guessed_letters']:
                if letter == "_":
                    unguessed_letters = True

            #if there are no more _ then player has won and game has ended
            if not unguessed_letters:
                self.dictionaries[ctx.author.id]['self.has_ended'] = True
                self.dictionaries[ctx.author.id]['self.has_won'] = True
                self.dictionaries[ctx.author.id]['self.game_started'] = False
            
            #if there are no more remaining guess, player loses and game has ended
            if self.dictionaries[ctx.author.id]['self.remaining_guesses'] < 1:
                self.dictionaries[ctx.author.id]['self.has_ended'] = True
                self.dictionaries[ctx.author.id]['self.has_won'] = False
                self.dictionaries[ctx.author.id]['self.game_started'] = False

            #status of the game
            #edits the original message 
            #much cleaner than spamming the channel
            await self.dictionaries[ctx.author.id]["self.edit_word"].edit(content=remainingletters(self, ctx))

    @commands.command()
    #get stats of the player
    #wins and losses
    async def stats(self, ctx):
        self.is_player = True
        with open('stats.txt') as f:
            author = str(ctx.author.id).replace(" ", "") 
            if author not in f.read():
                self.is_player = False

        #if player has played before, set their win and loss values
        if self.is_player == True:
           with open('stats.txt') as f:
                for line in f:
                    wins = line.strip().split()
                    author = str(ctx.author.id).replace(" ", "") 
                    if str(wins[0]) == author:
                        self.wins = int(wins[1])
                        self.losses = int(wins[2]) 
        #if player has not plyed before then set their values to 0
        if self.is_player == False:
            f = open('stats.txt', 'a')
            self.wins = 0
            self.losses = 0
            author = str(ctx.author.id).replace(" ", "") 
            f.write(author + ' ' + str(self.wins) + ' ' + str(self.losses) + "\n")
            f.close()

        await ctx.channel.send("`Wins: " + str(self.wins) + " Losses: " + str(self.losses) + "`")

#prints out letters of the word
def remainingletters(self, ctx):
    #if the player is guessing another players word
    if self.dictionaries[ctx.author.id]['self.own_word'] == True:
        status = ""
        if not self.has_ended:
            #sends to channel the word with guessed letters in it
            letters = ""
            for i in range(0, len(self.guessed_letters)):
                letters += '` ' + self.guessed_letters[i] + ' ` '
            status = '**{} guesses left** \n'.format(self.remaining_guesses)
            status += letters
        #if player wins and game ended
        if self.has_ended and self.has_won:
            status += '\n **You won! You correctly guessed** ' + '`{}`'.format(self.chosen_word)
        #if player loses and game ends
        elif self.has_ended and not self.has_won:
            status += '\n **You lost! The correct word was** ' + '`{}`'.format(self.chosen_word)
        return status

    #if player is guessing their own word
    else:
        status = ""
        #if game has not ended
        if not self.dictionaries[ctx.author.id]['self.has_ended']:
            #replace _ with correctly guessed letters
            #displays number of guesses left
            letters = ""
            for i in range(0, len(self.dictionaries[ctx.author.id]['self.guessed_letters'])):
                letters += '` ' + self.dictionaries[ctx.author.id]['self.guessed_letters'][i] + ' ` '
            status = '**{} guesses left** \n'.format(self.dictionaries[ctx.author.id]['self.remaining_guesses'])
            status += letters
        
        #win status, player wins adds one to their wins
        #edits text file to display updated wins
        if self.dictionaries[ctx.author.id]['self.has_ended'] and self.dictionaries[ctx.author.id]['self.has_won']:
            status += '\n **You won! You correctly guessed** `{}`\n+1 to wins'.format(self.dictionaries[ctx.author.id]['self.chosen_word'])
            self.wins += 1

            reading_file = open("stats.txt", "r")
            new_file_content = ""

            for line in reading_file:
                stripped_line = line.strip()
                wins = stripped_line.split()
                author = str(ctx.author.id).replace(" ", "") 
                if str(wins[0]) == author:
                    wins[1] = str(self.wins)
                    new_line = ' '.join(wins)
                    new_file_content += new_line + "\n"
                else:
                    new_line = stripped_line
                    new_file_content += new_line + "\n"
            reading_file.close()

            writing_file = open("stats.txt", "w")
            writing_file.write(new_file_content)
            writing_file.close()

            self.dictionaries[ctx.author.id]["self.own_word"] = True
            self.dictionaries[ctx.author.id]["self.game_started"] = False
        #lose status, +1 to losses
        #edits text file to display updated losses
        elif self.dictionaries[ctx.author.id]['self.has_ended'] and not self.dictionaries[ctx.author.id]['self.has_won']:
            status += '\n **You lost! The correct word was** `{}`\n+1 to losses'.format(self.dictionaries[ctx.author.id]['self.chosen_word'])
            self.losses += 1
            reading_file = open("stats.txt", "r")
            new_file_content = ""

            for line in reading_file:
                stripped_line = line.strip()
                wins = stripped_line.split()
                author = str(ctx.author.id).replace(" ", "") 
                if str(wins[0]) == author:
                    wins[2] = str(self.losses)
                    new_line = ' '.join(wins)
                    new_file_content += new_line + "\n"
                else:
                    new_line = stripped_line
                    new_file_content += new_line + "\n"
            reading_file.close()

            writing_file = open("stats.txt", "w")
            writing_file.write(new_file_content)
            writing_file.close()

            self.dictionaries[ctx.author.id]["self.own_word"] = True
            self.dictionaries[ctx.author.id]["self.game_started"] = False
        return status

def setup(bot):
    bot.add_cog(Hangman(bot))
    print('Hangman is loaded')