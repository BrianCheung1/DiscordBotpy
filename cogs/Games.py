import discord
from discord.ext import commands
from datetime import datetime


class Games(commands.Cog):
    """Makes Display For Games Look Better"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command(aliases=["games", "ga"])
    async def game(self, ctx, game_title, direct_download, steam_link, notes=None):
        """Displays games in embed"""
        game_title_fixed = game_title.replace("-", " ")
        embed = discord.Embed(
            title=f"Google Sheets Updated with {game_title_fixed}", color=ctx.author.color)
        embed.add_field(name="Direct Download: ",
                        value=direct_download, inline=False)
        embed.add_field(name="Steam Link: ", value=steam_link, inline=False)
        embed.add_field(name="Google Sheets: ",
                        value="https://docs.google.com/spreadsheets/d/1Qlw02EessdbkTKuPPiXquPdAEtNnUXC1oBYfGk0Y13A/edit#gid=2000315673", inline=False)
        notes_fixed = notes.replace("-", "\n")

        embed.add_field(name="Notes: ",
                        value=notes_fixed, inline=False)
        embed.set_footer(
            text="Time of Update [" + datetime.now().strftime("%I:%M %p") + "]")
        await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))
    print('Games is loaded')
