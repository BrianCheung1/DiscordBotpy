import asyncio
import discord
import youtube_dl
from discord.ext import commands
from functools import partial

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5, requester):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

        self.requester = requester

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False, stream=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data, requester=ctx.author)


class Music(commands.Cog):
    """Plays Music In Channel Of User"""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.command(aliases=['connect'])
    async def join(self, ctx, *arg):
        if ctx.author.voice is None:
            await ctx.channel.send("You're not connected to a voice channel")

        else:
            if ctx.voice_client is not None:
                channel = ctx.author.voice.channel
                return await ctx.voice_client.move_to(channel)
                await channel.connect()
            elif ctx.voice_client is None:
                channel = ctx.author.voice.channel
                await channel.connect()

    @commands.command(aliases=['stop'])
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
        except AttributeError:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.voice_client.disconnect()

    @commands.command(aliases=['play'])
    async def yt(self, ctx, *, search: str):
        """Plays from a url (almost anything youtube_dl supports)"""
        async with ctx.typing():
            if ctx.author.voice is None:
                await ctx.channel.send("You're not connected to a voice channel")

            else:
                if ctx.voice_client is not None:
                    channel = ctx.author.voice.channel
                    return await ctx.voice_client.move_to(channel)
                elif ctx.voice_client is None:
                    channel = ctx.author.voice.channel
                    await channel.connect()

            player = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

            ctx.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(name='pause')
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!')
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: Paused the song!')

    @commands.command(name='resume')
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!')
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**`{ctx.author}`**: Resumed the song!')

    @commands.command(name='skip')
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f'**`{ctx.author}`**: Skipped the song!')

    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        await ctx.channel.send(f'**Now Playing:** `{vc.source.title}` requested by '
                               f'`{vc.source.requester}`')


def setup(bot):
    bot.add_cog(Music(bot))
    print("Music is Loaded")


def setup(bot):
    bot.add_cog(Music(bot))
    print("Music is Loaded")
