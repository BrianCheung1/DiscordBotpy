import discord
from discord.ext import commands
import asyncio
import requests
from datetime import date
from datetime import datetime, timedelta
import datetime
import matplotlib.pyplot as plt
import os
from discord.ext import tasks


class Bitcoin(commands.Cog):
    """Shows Price of Bitcoin"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    # market price of crypto
    # defaults btc/eth/ltc
    # user can also provide their own coin to check marketplace
    @commands.command(aliases=['btc', 'eth', 'ltc', 'doge', 'cry'])
    async def crypto(self, ctx, arg=None):
        """fetches a crypto coin current price"""

        # COINBASE API
        if not arg:
            btc = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot').json()['data']
            eth = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot').json()['data']
            ltc = requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot').json()['data']
            embed = discord.Embed(title="Cryptocurrency Prices", color=ctx.author.color)
            embed.set_thumbnail(url='https://i.imgur.com/M6P1II5.png')
            embed.add_field(name="BTC: ", value="` " + as_currency((float(btc["amount"]))) + " ` ", inline=False)
            embed.add_field(name="ETH: ", value="` " + as_currency((float(eth["amount"]))) + " ` ", inline=False)
            embed.add_field(name="LTC: ", value="` " + as_currency((float(ltc["amount"]))) + " ` ", inline=False)
            embed.set_footer(text="Powered by Coinbase")
            await ctx.send(content=None, embed=embed)
        else:
            coin = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot'.format(arg.upper())).json()
            embed = discord.Embed(title="{} Price".format(arg.upper()), color=ctx.author.color)
            embed.set_thumbnail(url='https://i.imgur.com/M6P1II5.png')
            try:
                embed.add_field(name="{}: ".format(arg.upper()),
                                value="` " + as_currency((float(coin['data']["amount"]))) + " ` ", inline=False)
                embed.set_footer(text="Powered by Coinbase")
                await ctx.send(content=None, embed=embed)
            except KeyError:
                await ctx.send("Crypto coin not found or API limit Reached")

    @commands.command(aliases=['hist'])
    async def history(self, ctx, arg='btc', arg1=None):
        """fetches a crypto coin history price"""

        today = date.today() + timedelta(days=1)

        yesterday = today - timedelta(days=1)
        yesterday_est = date.today() - timedelta(days=1)

        lastweek = today - timedelta(days=7)
        lastweek_est = date.today() - timedelta(days=7)

        lastmonth = today - timedelta(days=30)
        lastmonth_est = date.today() - timedelta(days=30)

        try:
            price_now = float(
                requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot'.format(arg)).json()[
                    'data'][
                    'amount'])
        except KeyError:
            await ctx.send("Invalid Coin/Input - Correct Input : `hist {Crypto Coin} {YYYY-MM-DD}")
            return

        daily = (price_now - float(
            requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, yesterday)).json()[
                'data']['amount'])) / float(
            requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, yesterday)).json()[
                'data']['amount'])

        weekly = (price_now - float(
            requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, lastweek)).json()[
                'data']['amount'])) / float(
            requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, lastweek)).json()[
                'data']['amount'])

        monthly = (price_now - float(
            requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, lastmonth)).json()[
                'data']['amount'])) / float(
            requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, lastmonth)).json()[
                'data']['amount'])

        # if no date added to arguments
        if not arg1:
            # first date format is UTC
            # second date format is EST

            embed = discord.Embed(title="{} Price History".format(arg.upper()), color=ctx.author.color,
                                  description='Prices are taken from coinbase at 7pm')
            embed.set_thumbnail(url='https://i.imgur.com/M6P1II5.png')

            try:
                rate = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot'.format(arg)).json()[
                    'data']
                embed.add_field(name='Price now: ',
                                value="` " + as_currency(float(rate['amount'])) + " `", inline=False)
            except KeyError:
                await ctx.send("Invalid Coin/Input - Correct Input : `hist {Crypto Coin} {YYYY-MM-DD}")
                return

            # # if day hasn't reached 7pm will print price of coin now
            # try:
            #     rate = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, today)).json()[
            #         'data']
            #     embed.add_field(name='Price Today: ', value="` " + as_currency(float(rate['amount'])) + " `",
            #                     inline=False)
            # except KeyError:
            #     # if coin does not exist will price error
            #     try:
            #         rate = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot'.format(arg)).json()['data']
            #         embed.add_field(name='Price Today: ', value="` " + as_currency(float(rate['amount'])) + " `",
            #                         inline=False)
            #     except KeyError:
            #         await ctx.send("Invalid Coin/Input - Correct Input : `hist {Crypto Coin} {YYYY-MM-DD}")

            rate = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, yesterday)).json()[
                'data']
            embed.add_field(name='Price on {}: '.format(yesterday_est),
                            value="` " + as_currency(float(rate['amount'])) + " `", inline=False)

            rate = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, lastweek)).json()[
                'data']
            embed.add_field(name='Price on {}: '.format(lastweek_est),
                            value="` " + as_currency(float(rate['amount'])) + " `", inline=False)

            rate = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, lastmonth)).json()[
                'data']
            embed.add_field(name='Price on {}: '.format(lastmonth_est),
                            value="` " + as_currency(float(rate['amount'])) + " `", inline=False)

            embed.add_field(name='Daily Percent Change: ',
                            value="` " + str('{:.2%}'.format(daily)) + " `", inline=True)
            embed.add_field(name='Weekly Percent Change: ',
                            value="` " + str('{:.2%}'.format(weekly)) + " `", inline=True)
            embed.add_field(name='Monthly Percent Change: ',
                            value="` " + str('{:.2%}'.format(monthly)) + " `", inline=True)

            embed.set_footer(text="Powered by Coinbase")
            await ctx.send(content=None, embed=embed)

        # if users wants to check a certain date and coin
        else:
            try:
                datetime.datetime.strptime(arg1, '%Y-%m-%d')
            except ValueError:
                await ctx.send("Incorrect data format, should be YYYY-MM-DD")
                return

            # adds one day to argument to compensate est to utc
            arg1UTC = datetime.datetime.strptime(arg1, '%Y-%m-%d') + timedelta(days=1)
            today = date.today() + timedelta(days=1)

            embed = discord.Embed(title="{} Price History".format(arg.upper()), color=ctx.author.color,
                                  description='Prices are taken from coinbase at 7pm')
            embed.set_thumbnail(url='https://i.imgur.com/M6P1II5.png')

            # will try to receive exchange price of 7pm, if error will print price of coin now
            try:
                rate = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot'.format(arg)).json()[
                    'data']
                embed.add_field(name='Price now: ',
                                value="` " + as_currency(float(rate['amount'])) + " `", inline=False)
            except KeyError:
                await ctx.send("Invalid Coin/Input - Correct Input : `hist {Crypto Coin} {YYYY-MM-DD}")
                return

            # print out price of user inputted coin at user inputted date
            rate = requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot?date={}'.format(arg, arg1UTC)).json()[
                'data']
            embed.add_field(name='Price on {}: '.format(arg1), value="` " + as_currency(float(rate['amount'])) + " `",
                            inline=False)

            date_change = (price_now - float(rate['amount'])) / float(rate['amount'])

            embed.add_field(name='Percent Change: ',
                            value="` " + str('{:.2%}'.format(date_change)) + " `", inline=True)
            embed.set_footer(text="Powered by Coinbase")
            await ctx.send(content=None, embed=embed)

    @commands.command()
    async def plot(self, ctx):
        price_now = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot').json()[
                              'data']['amount'])
        yesterday = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot?date=2021-01-03').json()[
                              'data']['amount'])
        yesterday_yesterday = float(
            requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot?date=2021-01-02').json()[
                'data']['amount'])
        plt.plot([yesterday_yesterday, yesterday, price_now])
        plt.annotate(as_currency(yesterday_yesterday),
                     (0, yesterday_yesterday),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center')

        price_now -= price_now % -10000
        plt.axis([0, 6, 0, price_now])

        plt.title('Bitcoin\'s Graph')
        plt.xlabel('Dates')
        plt.ylabel('Prices')

        plt.savefig(fname='plot')
        await ctx.send(file=discord.File('plot.png'))
        plt.clf()
        os.remove('plot.png')

    @commands.command(aliases=['ex'])
    async def exchange(self, ctx, arg=0.0, arg1='BTC'):

        rate = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot').json()[
                         'data']['amount'])
        embed = discord.Embed(title="Crypto Exchange Rates", color=ctx.author.color)
        embed.set_thumbnail(url='https://i.imgur.com/M6P1II5.png')

        if arg == 0 and arg1 is 'BTC':
            converted_price = arg * rate
            embed.add_field(name='Rate: ', value='` {} ` BTC to USD: ` {} `'.format(arg, as_currency(converted_price)))
            await ctx.send(content=None, embed=embed)
        elif arg != 0 and arg1 is 'BTC':
            converted_price = arg * rate
            embed.add_field(name='Rate: ', value='` {} ` BTC to USD: ` {} `'.format(arg, as_currency(converted_price)))
            await ctx.send(content=None, embed=embed)
        elif arg != 0 and arg1 != 'BTC':
            rate = float(requests.get('https://api.coinbase.com/v2/prices/{}-USD/spot'.format(arg1)).json()[
                             'data']['amount'])
            converted_price = arg * rate
            embed.add_field(name='Rate: ', value='` {} ` {} to USD: ` {} `'.format(arg, arg1.upper(),  as_currency(converted_price)))
            await ctx.send(content=None, embed=embed)

# converts floats in dollar amount
def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)


def setup(bot):
    bot.add_cog(Bitcoin(bot))
    print('Bitcoin is loaded')
