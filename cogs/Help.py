import discord
from discord.ext import commands
import asyncio
import random

# class Help(commands.Cog):
#     """Prints out information about commands"""

#     def __init__(self, bot, *args, **kwargs):
#         self.bot = bot

#     @commands.command()
#     async def help(self, ctx, *input):
#         if not input:
#             embed = discord.Embed(
#                 title="Commands", description='Information on commands', colour=ctx.author.colour)
#             embed.set_thumbnail(url=ctx.author.avatar_url)
#             embed.add_field(name='``balance`', value="Shows balance of user")
#             embed.add_field(name='``bj *amount`',
#                             value="Starts a game of blackjack, optional: bet amount")
#             embed.add_field(name='``crypto *symbol`',
#                             value="Shows the price of crpyto currency")
#             embed.add_field(name='``dog`', value="Provides random dog fact")
#             embed.add_field(name='``exchange`',
#                             value="Shows exchange rate of entered crypto to USD")
#             embed.add_field(name='``flip`', value="Flip a coin heads or tail")
#             embed.add_field(name='``hangman`',
#                             value="starts a game of hangman")
#             embed.add_field(name='``help`', value="Display this embed")
#             embed.add_field(name='``history *symbol *date`',
#                             value="Displays past prices of crypto currency")
#             embed.add_field(name='``mute`', value="mutes all user in channel")
#             embed.add_field(name='``profile`',
#                             value="Display information on user")
#             embed.add_field(
#                 name='``users`', value="Returns number of total users, online users, offline users")
#             embed.add_field(
#                 name='``roll [number]`', value="Roll a dice, default 1-6, can add a number at the end to roll 1-#")
#             embed.add_field(name='``rps`', value="Play a game of rps")
#             embed.add_field(name='``russian`',
#                             value="Play a game of russian roulette")
#             embed.add_field(
#                 name='``spam [@user] *text *amount`', value="spams a user mentioned")
#             embed.add_field(name='``stats`', value="Shows stats for hangman")
#             embed.add_field(name='``unmute`',
#                             value="unmutes all user in channel")
#             embed.add_field(
#                 name='``urban [word]`', value="Provides urbandictionary definiton of given word")
#             embed.set_footer(text='* Represents optional arguments')
#             await ctx.channel.send(content=None, embed=embed)
#         else:
#             for cog in self.bot.cogs:
#                 # check if cog is the matching one
#                 if cog.lower() == input[0].lower():

#                     # making title - getting description from doc-string below class
#                     emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
#                                         color=discord.Color.green())

#                     # getting commands from cog
#                     for command in self.bot.get_cog(cog).get_commands():
#                         # if cog is not hidden
#                         if not command.hidden:
#                             emb.add_field(
#                                 name=f"`{command.name}`", value=command.help, inline=False)
#                     # found cog - breaking loop
#                     break

#             # if input not found
#             # yes, for-loops have an else statement, it's called when no 'break' was issued
#             else:
#                 emb = discord.Embed(title="What's that?!",
#                                     description=f"I've never heard from a module called `{input[0]}` before :scream:",
#                                     color=discord.Color.orange())
#             await ctx.channel.send(content=None, embed=emb)


async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """Sends this help message"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """Shows all modules of that bot"""

        # !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
        prefix = '`'  # ENTER YOUR PREFIX - loaded from config, as string or how ever you want!
        version = '1'  # enter version of your code

        # setting owner name - if you don't wanna be mentioned remove line 49-60 and adjust help text (line 88)
        owner = '706279634672549989'  # ENTER YOU DISCORD-ID
        owner_name = 'butter#4293'  # ENTER YOUR USERNAME#1234

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            # starting to build embed
            emb = discord.Embed(title='Commands and modules', color=random_color(),
                                description=f'Use `{prefix}help <module>` for commands'
                                            f':eyes:\n')
            emb.set_thumbnail(url='https://i.imgur.com/h6TUQLa.jpg')
            # iterating trough cogs, gathering descriptions
            cogs_desc = ''
            cogs_list = ['MessageLogger', 'Options',
                         'SlotMachine', 'ReactionRoles', "BotReady"]
            for cog in self.bot.cogs:
                if cog not in cogs_list:
                    cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # adding 'list' of cogs to embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # setting information about author
            emb.add_field(name="About", value=f"The Bots is developed by {owner_name}, based on discord.py.\n\
                                    This version of it is maintained by {owner_name}\n\
                                    Please visit https://github.com/BrianCheung1/DiscordBotpy to submit ideas or bugs.")
            emb.set_footer(text=f"Bot is running {version}")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = discord.Embed(title=f'Commands in {cog}', description=self.bot.cogs[cog].__doc__,
                                        color=random_color())
                    emb.set_thumbnail(url='https://i.imgur.com/h6TUQLa.jpg')
                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(
                                name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = discord.Embed(title="Modules Not Found",
                                    description=f"`{input[0]}` was not found in the system",
                                    color=random_color())
                emb.set_thumbnail(url='https://i.imgur.com/h6TUQLa.jpg')

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(title="Too Many Modules Provided",
                                description="Please request only one module at once :sweat_smile:",
                                color=random_color())
            emb.set_thumbnail(url='https://i.imgur.com/h6TUQLa.jpg')
        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(Help(bot))
    print("Help is loaded")


def random_color():
    list_of_colors = [discord.Color.blue(), discord.Color.blurple(),
                      discord.Color.dark_blue(), discord.Color.dark_gold(), discord.Color.dark_gray(), discord.Color.dark_green(), discord.Color.dark_grey(), discord.Color.dark_magenta(), discord.Color.dark_orange(), discord.Color.dark_purple(), discord.Color.dark_red(), discord.Color.dark_teal(), discord.Color.dark_theme(), discord.Color.darker_gray(), discord.Color.default(), discord.Color.gold(), discord.Color.green(), discord.Color.greyple(), discord.Color.light_gray(), discord.Color.lighter_gray(), discord.Color.magenta(), discord.Color.orange(), discord.Color.purple(), discord.Color.red(), discord.Color.teal()]
    return random.choice(list_of_colors)
