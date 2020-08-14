import discord
from discord.ext import commands
import asyncio
import random

class Blackjack(commands.Cog):
    """Plays a game of blackjack"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        #self.first_card = randomcards()
        #self.second_card = randomcards()
        #self.starting_hand = str(self.first_card) + " " + str(self.second_card)
        #self.total = 0
        #self.busted = False
        self.player = ""
        self.dictionaries = {}

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
           
        embed = discord.Embed(title="Balance", description='Top Players Balance', colour=ctx.author.colour)
        with open('balance.txt') as f:
            f = f.read()
            f = [l.split() for l in f.splitlines()]
            f = sorted(f, key=lambda kv: int(kv[1]), reverse=True)
            x = 1
            for line in f:
                player = line[0]
                balance = line[1]
                member = ctx.author.guild.get_member(int(player))
                embed.add_field(name= str(x) + ". ` " + str(member) + " `", value="Balance: $" + str(balance), inline=False)
                x += 1
                if x == 11:
                    break
        await ctx.send(embed= embed)
        
    @commands.Cog.listener()
    #returns time that command needs before it can be used again
    async def on_command_error(self, ctx, error):
        #Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f' You must wait {int(s)} seconds to use this command!')
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Hey! You lack permission to use this command.")
        raise error
    

    @commands.command()
    @commands.cooldown(rate=1, per=3600, type=commands.BucketType.user)
    #provides user with daily balance
    async def daily(self, ctx):
        if ctx.author.id not in self.dictionaries:
            self.dictionaries[ctx.author.id] = {
            "self.money_balance": 1000,
            "self.game_started" : False
            }

        self.is_player = True
        with open('balance.txt') as f:
            author = str(ctx.author.id).replace(" ", "") 
            if author not in f.read():
                self.is_player = False
        
        #if user does exist, add 500 to their balance
        if self.is_player == True:
            with open('balance.txt') as f:
                for line in f:
                    author = str(ctx.author.id).replace(" ", "") 
                    balance = line.strip().split()
                    if str(balance[0]) == author:
                        if ctx.author.id not in self.dictionaries:
                            self.dictionaries[ctx.author.id] = {
                            "self.money_balance" : int(balance[1])
                            }
                        self.dictionaries[ctx.author.id]["self.money_balance"] = int(balance[1])

            reading_file = open("balance.txt", "r")
            new_file_content = ""

            for line in reading_file:
                stripped_line = line.strip()
                balance = stripped_line.split()
                author = str(ctx.author.id).replace(" ", "")
                if str(balance[0]) == author:
                    self.dictionaries[ctx.author.id]["self.money_balance"] += 500
                    balance[1] = str(self.dictionaries[ctx.author.id]["self.money_balance"])
                    new_line = ' '.join(balance)
                    new_file_content += new_line + "\n"
                else:
                    new_line = stripped_line
                    new_file_content += new_line + "\n"

            reading_file.close()

            writing_file = open("balance.txt", "w")
            writing_file.write(new_file_content)
            writing_file.close()

        #if user doesn't exist in file then give them 500 on top of default value
        if self.is_player == False:
            self.dictionaries[ctx.author.id]["self.money_balance"] += 500
            f = open('balance.txt', 'a')
            author = str(ctx.author.id).replace(" ", "") 
            f.write(author + ' ' + str(self.dictionaries[ctx.author.id]["self.money_balance"]) + "\n")
            f.close()

        await ctx.channel.send("`Balance: $" + str(self.dictionaries[ctx.author.id]["self.money_balance"]) + "`")
    
            

    @commands.command(aliases=['blackjack', 'black'])
    #starts a game of blackjack
    async def bj(self, ctx, arg = 100, members: discord.Member=None):
    
        #if a new player, then provide them with default values
        if ctx.author.id not in self.dictionaries:
            self.dictionaries[ctx.author.id] = {
            "self.money_balance" : 1000,
            "self.first_card" : randomcards(),
            "self.second_card" : randomcards(),
            "self.starting_hand" : "",
            "self.total": 0,
            "self.dealers_total" : 0,
            "self.busted" : False,
            "self.player" : ctx.author.id,
            "self.has_stay" : False,
            "self.dealers_busted" : False,
            "self.has_ended"  : False,
            "self.dealers_first_card" : randomcards(),
            "self.dealers_second_card" : randomcards(),
            "self.edit_cards": "",
            "self.bet": arg,
            "self.game_started": False,
            "self.extra_card": 0,
            "self.dealers_extra_card": 0
            }

        self.is_player = True
        with open('balance.txt') as f:
            author = str(ctx.author.id).replace(" ", "") 
            if author not in f.read():
                self.is_player = False
        
        if self.is_player == True:
            with open('balance.txt') as f:
                for line in f:
                    author = str(ctx.author.id).replace(" ", "") 
                    balance = line.strip().split()
                    if str(balance[0]) == author:
                        self.dictionaries[ctx.author.id]["self.money_balance"] = int(balance[1])

            if self.dictionaries[ctx.author.id]["self.game_started"]:
                self.dictionaries[ctx.author.id]["self.money_balance"] -= int(arg / 2)
                changebalance(self,ctx)

        if self.is_player == False:
            f = open('balance.txt', 'a')
            if ctx.author.id not in self.dictionaries:
                self.dictionaries[ctx.author.id] = {
                "self.money_balance" : 1000
                }
            author = str(ctx.author.id).replace(" ", "") 
            f.write(author + ' ' + str(self.dictionaries[ctx.author.id]["self.money_balance"]) + "\n")
            f.close()

        #if they have already played,reset their values
        if ctx.author.id in self.dictionaries:
            self.dictionaries[ctx.author.id]["self.first_card"] = randomcards()
            self.dictionaries[ctx.author.id]["self.second_card"] = randomcards()
            self.dictionaries[ctx.author.id]["self.starting_hand"] = ""
            self.dictionaries[ctx.author.id]["self.total"]= 0
            self.dictionaries[ctx.author.id]["self.dealers_total"] = 0
            self.dictionaries[ctx.author.id]["self.busted"] = False
            self.dictionaries[ctx.author.id]["self.player"] = ctx.author.id
            self.dictionaries[ctx.author.id]["self.has_stay"] = False
            self.dictionaries[ctx.author.id]["self.dealers_busted"] = False
            self.dictionaries[ctx.author.id]["self.has_ended"] = False
            self.dictionaries[ctx.author.id]["self.dealers_first_card"] = randomcards()
            self.dictionaries[ctx.author.id]["self.dealers_second_card"] = randomcards()
            self.dictionaries[ctx.author.id]["self.edit_cards"] = ""
            self.dictionaries[ctx.author.id]["self.bet"] = arg
            self.dictionaries[ctx.author.id]["self.game_started"] = True
            self.dictionaries[ctx.author.id]["self.extra_card"] = 0
            self.dictionaries[ctx.author.id]["self.dealers_extra_card"] = 0
        
        if self.dictionaries[ctx.author.id]["self.bet"] > self.dictionaries[ctx.author.id]["self.money_balance"]:
            await ctx.channel.send("You don't have enough money")
            self.dictionaries[ctx.author.id]["self.game_started"] = False
            return

        #starting hand of the player, dealer hand
        self.dictionaries[ctx.author.id]["self.starting_hand"] = str(convertcards(self.dictionaries[ctx.author.id]["self.first_card"])) + " " + str(convertcards(self.dictionaries[ctx.author.id]["self.second_card"]))
        self.dictionaries[ctx.author.id]["self.dealers_starting_hand"] = str(convertcards(self.dictionaries[ctx.author.id]["self.dealers_first_card"]))

        #if player has an ace it is converted to 11 if total of both cards is less then 10
        if self.dictionaries[ctx.author.id]["self.first_card"] == 1 and self.dictionaries[ctx.author.id]["self.second_card"] <= 10:
            self.dictionaries[ctx.author.id]["self.first_card"] = 11
        if self.dictionaries[ctx.author.id]["self.second_card"]  == 1 and self.dictionaries[ctx.author.id]["self.first_card"] <= 10:
            self.dictionaries[ctx.author.id]["self.second_card"] = 11

        #not sure if needed
        if self.dictionaries[ctx.author.id]["self.dealers_first_card"] == 1 and self.dictionaries[ctx.author.id]["self.dealers_first_card"] <= 10:
            self.dictionaries[ctx.author.id]["self.dealers_first_card"] = 11


        #set the total of the player hand and the dealer hand
        self.dictionaries[ctx.author.id]["self.total"] += self.dictionaries[ctx.author.id]["self.first_card"] + self.dictionaries[ctx.author.id]["self.second_card"]
        self.dictionaries[ctx.author.id]["self.dealers_total"] += self.dictionaries[ctx.author.id]["self.dealers_first_card"]

        embed = hands(self, ctx)

        #sets the hand to be edited later on
        self.dictionaries[ctx.author.id]["self.edit_cards"] = await ctx.channel.send(embed=embed)
        #await self.start_message.add_reaction('✅')
        embed = discord.Embed(title="Rules", description='Information on Blackjack')
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='`bj [amount]', value="Start a game of blackjack with bet amount, [Default Bet = $100]",inline=False)
        embed.add_field(name='`hit', value="Adds another card to your hand",inline=False)
        embed.add_field(name='`stand', value="Keep cards and let dealer play", inline=False)
        embed.add_field(name='`balance', value="Show your balance", inline=False)
        embed.add_field(name='Win conditions', value = "Player higher total -> +$100\nDealer bust -> +$100\nPlayer Bust -> -$150\nDealer higher total -> -$100")
        await ctx.channel.send(content=None, embed=embed)

        if self.dictionaries[ctx.author.id]["self.total"] == 21:
            self.dictionaries[ctx.author.id]["self.money_balance"] += int(self.dictionaries[ctx.author.id]["self.bet"] * 1.5)
            changebalance(self,ctx)
            self.dictionaries[ctx.author.id]["self.busted"] = False
            self.dictionaries[ctx.author.id]["self.has_ended"] = True
            await ctx.channel.send("`Player got Blackjack`, bj to start a new game \n" + "Balance: $" + str(self.dictionaries[ctx.author.id]["self.money_balance"]))
            self.dictionaries[ctx.author.id]["self.game_started"] = False


    @commands.command()
    #allows the player to get another card
    async def hit(self, ctx):
        if self.dictionaries[ctx.author.id]["self.has_stay"] == True:
            return
        if self.dictionaries[ctx.author.id]["self.has_ended"] == True:
            return

        #if player or dealer busted, new game must be started
        if self.dictionaries[ctx.author.id]["self.busted"] == True or self.dictionaries[ctx.author.id]["self.dealers_busted"] == True:
            await ctx.channel.send("`bj to start a new game")
            return


        #adds a new card to the player hand and adds to the total
        extra_card = randomcards()

        if self.dictionaries[ctx.author.id]["self.extra_card"] == 11:
            if self.dictionaries[ctx.author.id]["self.extra_card"] + extra_card + self.dictionaries[ctx.author.id]["self.total"] > 21:
                self.dictionaries[ctx.author.id]["self.total"] -= 10

        self.dictionaries[ctx.author.id]["self.starting_hand"] += " " + str(convertcards(extra_card))

        if extra_card == 1 and self.dictionaries[ctx.author.id]["self.total"] <= 10:
           extra_card = 11
        
        self.dictionaries[ctx.author.id]["self.total"] += extra_card

        self.dictionaries[ctx.author.id]["self.extra_card"] = extra_card

        #if total is more than 21, set value of first card back to 1 and -10 from total
        if self.dictionaries[ctx.author.id]["self.first_card"] == 11 and self.dictionaries[ctx.author.id]["self.total"] > 21:
            self.dictionaries[ctx.author.id]["self.first_card"] = 1
            self.dictionaries[ctx.author.id]["self.total"] -= 10
        if self.dictionaries[ctx.author.id]["self.second_card"] == 11 and self.dictionaries[ctx.author.id]["self.total"] > 21:
            self.dictionaries[ctx.author.id]["self.second_card"] = 1
            self.dictionaries[ctx.author.id]["self.total"] -= 10


        embed = hands(self,ctx)
        #edits teh original message to add a new card
        await self.dictionaries[ctx.author.id]["self.edit_cards"].edit(embed = embed)
        #await ctx.channel.send(hands(self,ctx))
        
        #if player total goes over 21, they have lost
        if self.dictionaries[ctx.author.id]["self.total"] > 21:
            self.dictionaries[ctx.author.id]["self.money_balance"] -= self.dictionaries[ctx.author.id]["self.bet"]
            changebalance(self,ctx)
            self.dictionaries[ctx.author.id]["self.busted"] = True
            self.dictionaries[ctx.author.id]["self.has_ended"] = True
            await ctx.channel.send("`Player bust, Dealer wins`, bj to start a new game \n" + "Balance: $" + str(self.dictionaries[ctx.author.id]["self.money_balance"]))
            self.dictionaries[ctx.author.id]["self.game_started"] = False
    
    @commands.command(aliases=['stay'])
    #player decides to stay, so dealer plays now
    async def stand(self, ctx):
        if ctx.author.id != self.dictionaries[ctx.author.id]["self.player"]:
            return
        if self.dictionaries[ctx.author.id]["self.has_ended"] == True or self.dictionaries[ctx.author.id]["self.busted"] == True:
            return

        self.dictionaries[ctx.author.id]["self.dealer_extra_card"] = 0
        #while dealer is less than 17, and less than player total, add another card
        self.dictionaries[ctx.author.id]["self.has_stay"] = True 
        if self.dictionaries[ctx.author.id]["self.busted"] == False:
            while self.dictionaries[ctx.author.id]["self.dealers_total"] < 17:
                await asyncio.sleep(.5)
                dealers_extra_card = randomcards()
                self.dictionaries[ctx.author.id]["self.dealers_starting_hand"] += " " + str(convertcards(dealers_extra_card))
                
                if self.dictionaries[ctx.author.id]["self.dealer_extra_card"] == 11 and self.dictionaries[ctx.author.id]["self.dealers_total"] + dealers_extra_card > 21:
                    self.dictionaries[ctx.author.id]["self.dealers_total"] -= 10
                if self.dictionaries[ctx.author.id]["self.dealers_first_card"] == 11 and self.dictionaries[ctx.author.id]["self.dealers_total"] + dealers_extra_card > 21:
                    self.dictionaries[ctx.author.id]["self.dealers_total"] -= 10

                if dealers_extra_card == 1 and self.dictionaries[ctx.author.id]["self.dealers_total"] <= 10:
                    dealers_extra_card = 11

                self.dictionaries[ctx.author.id]["self.dealers_total"] += dealers_extra_card
         
                self.dictionaries[ctx.author.id]["self.dealer_extra_card"] = dealers_extra_card

                embed = hands(self,ctx)
                await self.dictionaries[ctx.author.id]["self.edit_cards"].edit(embed = embed)
        
        #win conditions
        #if dealer hand goes over 21, dealer loses
        if self.dictionaries[ctx.author.id]["self.dealers_total"] > 21:
            self.dictionaries[ctx.author.id]["self.dealers_busted"] = True
            self.dictionaries[ctx.author.id]["self.has_ended"] = True
            self.dictionaries[ctx.author.id]["self.money_balance"] += self.dictionaries[ctx.author.id]["self.bet"]
            changebalance(self, ctx)
            self.dictionaries[ctx.author.id]["self.game_started"] = False
            await ctx.channel.send("`Dealer bust, Player Wins`, bj to start a new game \n" + "Balance: $" + str(self.dictionaries[ctx.author.id]["self.money_balance"]))

        #if dealer total is higher than player total, dealer wins
        if self.dictionaries[ctx.author.id]["self.dealers_total"] > self.dictionaries[ctx.author.id]["self.total"] and self.dictionaries[ctx.author.id]["self.dealers_total"] <= 21:
            self.dictionaries[ctx.author.id]["self.money_balance"] -= self.dictionaries[ctx.author.id]["self.bet"]
            self.dictionaries[ctx.author.id]["self.has_ended"] = True
            changebalance(self, ctx)
            self.dictionaries[ctx.author.id]["self.game_started"] = False
            await ctx.channel.send("`Dealer wins`, bj to start a new game \n" + "Balance: $" + str(self.dictionaries[ctx.author.id]["self.money_balance"]))


        #if dealer total is less than player total, dealer loses
        if self.dictionaries[ctx.author.id]["self.dealers_total"] < self.dictionaries[ctx.author.id]["self.total"] and self.dictionaries[ctx.author.id]["self.dealers_total"] <= 21:
            self.dictionaries[ctx.author.id]["self.money_balance"] += self.dictionaries[ctx.author.id]["self.bet"]
            self.dictionaries[ctx.author.id]["self.has_ended"] = True
            changebalance(self, ctx)
            self.dictionaries[ctx.author.id]["self.game_started"] = False
            await ctx.channel.send("`Player wins`, bj to start a new game \n" + "Balance: $" + str(self.dictionaries[ctx.author.id]["self.money_balance"]))

        #if totals are equal, game is a tie
        if self.dictionaries[ctx.author.id]["self.dealers_total"] == self.dictionaries[ctx.author.id]["self.total"] and self.dictionaries[ctx.author.id]["self.dealers_total"] <= 21:
            await ctx.channel.send("`Tie`, `bj to start a new game \n" + "Balance: $" + str(self.dictionaries[ctx.author.id]["self.money_balance"]))
            self.dictionaries[ctx.author.id]["self.game_started"] = False
            self.has_ended = True
            

    @commands.command()
    #returns balance of the user
    async def balance(self, ctx):
        #if user doesn't exist in dictionary give them a default value of 1k
        if ctx.author.id not in self.dictionaries:
            self.dictionaries[ctx.author.id] = {
            "self.money_balance": 1000,
            "self.game_started" : False
            }

        self.is_player = True
        with open('balance.txt') as f:
            author = str(ctx.author.id).replace(" ", "") 
            if author not in f.read():
                self.is_player = False
        
        if self.is_player == True:
            with open('balance.txt') as f:
                for line in f:
                    author = str(ctx.author.id).replace(" ", "") 
                    balance = line.strip().split()
                    if str(balance[0]) == author:
                        self.dictionaries[ctx.author.id]["self.money_balance"] = int(balance[1])

        if self.is_player == False:
            f = open('balance.txt', 'a')
            author = str(ctx.author.id).replace(" ", "") 
            f.write(author + ' ' + str(self.dictionaries[ctx.author.id]["self.money_balance"]) + "\n")
            f.close()

        await ctx.channel.send("`Balance: $" + str(self.dictionaries[ctx.author.id]["self.money_balance"]) + "`")
    

#draws a random card from the list
def randomcards():
    listofcards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    randomcard = random.choice(listofcards)
    return randomcard

#provides hands of both players
def hands(self, ctx):
    # status = ""
    # status += str(ctx.author.mention) + " Hand: " + self.dictionaries[ctx.author.id]["self.starting_hand"] + "\n"
    # status += "Total: " + str(self.dictionaries[ctx.author.id]["self.total"]) + "\n"
    # status += "Dealers Hand: " + self.dictionaries[ctx.author.id]["self.dealers_starting_hand"] + "\n"
    # status += "Total: " + str(self.dictionaries[ctx.author.id]["self.dealers_total"]) + "\n"

    embed = discord.Embed(title="Hands",colour = ctx.author.colour)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name='` ' + ctx.author.name + ' Hand: ` ', value=str(self.dictionaries[ctx.author.id]["self.starting_hand"]) + "\n` Total: " + str(self.dictionaries[ctx.author.id]["self.total"])+ " ` ", inline=False)
    embed.add_field(name='` Dealers Hand: ` ', value=str(self.dictionaries[ctx.author.id]["self.dealers_starting_hand"]) + "\n` Total: " + str(self.dictionaries[ctx.author.id]["self.dealers_total"]) + " ` ", inline=False)
    
    return embed
    


#convert cards to their emojis form
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
        card = random.choice(randomtencard)
    return card

#changes balance in textfile
def changebalance(self, ctx):
    reading_file = open("balance.txt", "r")
    new_file_content = ""

    for line in reading_file:
        stripped_line = line.strip()
        balance = stripped_line.split()
        author = str(ctx.author.id).replace(" ", "") 
        if str(balance[0]) == author:
            #replace balance in textfile with balance of the user
            balance[1] = str(self.dictionaries[ctx.author.id]["self.money_balance"])
            new_line = ' '.join(balance)
            new_file_content += new_line + "\n"
        else:
            new_line = stripped_line
            new_file_content += new_line + "\n"

    reading_file.close()

    writing_file = open("balance.txt", "w")
    writing_file.write(new_file_content)
    writing_file.close()
    


def setup(bot):
    bot.add_cog(Blackjack(bot))
    print('Blackjack is loaded')