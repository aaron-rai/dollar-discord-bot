#This music bot uses wavelink instead of FFMPEG
#Current commands:
#join, leave, play, skip, pause, resume, nowplaying, seek, volume, playskip, next, load, lyrics, stop
import discord
import os
import wavelink
import logging
import asyncio
import logging.handlers
import random

from pandas import *
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from lyricsgenius import Genius

#Global Variables
ADMIN = "⚡️"
DJ = "🎧"
run = True
artist = ""

#Create Unfiltered Bot to accept commands from other bots
class UnfilteredBot(commands.Bot):
    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)

client = UnfilteredBot(command_prefix="!", intents=discord.Intents.all())

#Create an instance of bot(for each bot instance to have its own queue)
class CustomPlayer(wavelink.Player):
    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()

#load environment
load_dotenv()

#Setup Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Get Discord and Genius token from ENV
DISCORD_TOKEN = os.getenv("TOKEN")
genius = Genius("GENIUSTOKEN")

#Wavelink setup
@client.event
async def on_ready():
    client.loop.create_task(connect_nodes())

async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=client,
        host='127.0.0.1',
        port=2333,
        password='discordTest123'
    )

#Events, load wavelink node, play next song in queue
@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    logger.info(f'Node: <{node.identifier}> is ready')
    logger.info(f'Logged in as {node.bot.user} ({node.bot.user.id})')
    await client.change_presence(activity=discord.Game(name=" Music!"))

@client.event
async def on_wavelink_track_start(player: CustomPlayer, track: wavelink.Track):
    global artist
    artist = track.author
    
@client.event
async def on_wavelink_track_end(player: CustomPlayer, track: wavelink.Track, reason):
    if not player.queue.is_empty:
        next_track = player.queue.get()
        await player.play(next_track)
        logger.info(f'Playing next track: {next_track}')
    else:
        logger.info('Queue is empty')

#Scan messages to ensure message was sent in #commands chat
@client.event
async def on_message(message):
    msg = message.content
    channel = str(message.channel)
    author = message.author
    
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        text = 'All of my commands are listed in the #commands chat in the mfDiscord, too add me to your discord or to get a list of commands, DM Cash#8915!'
        await message.channel.send(text)
        logger.info(f'{author} sent a DM to Dollar')
 

    if channel == 'commands' or channel == 'test':
        if msg.startswith('!'):
            logger.info(f'Bot command entered. Command: {msg} | Author: {author}')
            await client.process_commands(message)
        elif str(message.attachments) == "[]":
            await client.process_commands(message)
            logger.info(f'User message entered. Message: {msg} | Author: {author}')
        else:
            split_v1 = str(message.attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            if filename.endswith(".csv"):                                   # refactor if possible
                await message.attachments[0].save(fp='ex.csv')
                await message.channel.send('File Downloaded, use !load to load songs into queue.')
            logger.info(f'CSV successfully downloaded, author: {author}')
    elif msg.startswith('!clear'):
        await client.process_commands(message)
        logger.info(f"{author} used !clear")
    elif msg.startswith('!'):
        logger.info(f'Command entered in wrong channel, deleting: {msg}')
        await message.delete(delay = 1)

#When user joins a voice channel assign DJ role, and remove when they leave
#This prevents users not in a voice channel from making commands
@client.event
async def on_voice_state_update(member, before, after):
    ctxbefore = before.channel
    ctxafter = after.channel
    role = get(member.guild.roles, name=DJ)

    if ctxbefore is None and ctxafter is not None:
        await member.add_roles(role)
        logger.info(f"{member} joined {ctxafter} adding Dj role")
    elif ctxbefore is not None and ctxafter is None:
        await member.remove_roles(role)
        logger.info(f"{member} left {ctxbefore} removing Dj role")
    else:
        logger.error(f"{member} joined or left! Error adding or removing role")

#Join authors voice channel
@client.command(aliases=['Join'])
@commands.has_role(DJ or ADMIN)
async def join(ctx):
    vc = ctx.voice_client
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        return await ctx.send('You must be in a voice channel for the bot to connect.')
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)
        await vc.set_volume(5)#Set bot volume initially to 5
    else:
        await ctx.send('The bot is already connected to a voice channel')

#Leave voice channel
@client.command(aliases=['Leave'])
@commands.has_role(DJ)
async def leave(ctx):
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
        await ctx.channel.purge(limit=10000)
    else:
        await ctx.send('The bot is not connected to a voice channel.')

#Play a song, ex: !play starboy the weeknd
@client.command(aliases=['Play'])
@commands.has_role(DJ)
async def play(ctx, *, search: wavelink.YouTubeMusicTrack):
    vc = ctx.voice_client
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)
        await vc.set_volume(5)

    if vc.is_playing():
        vc.queue.put(item=search)
        embed = discord.Embed(title=search.title, url=search.uri, description=f"Added {search.title} to the Queue!", colour=discord.Colour.random())
        embed.set_author(name=f"{search.author}")
        embed.set_thumbnail(url=f"{search.thumbnail}")
        if vc.queue.is_empty:
            embed.set_footer(text="Queue is empty")
        else:
            nextitem = vc.queue.get()
            vc.queue.put_at_front(item=nextitem)
            embed.set_footer(text=f"Next song is: {nextitem}")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=search.title, url=search.uri, description=f"Now Playing {search.title}!", colour=discord.Colour.random())
        embed.set_author(name=f"{search.author}")
        embed.set_thumbnail(url=f"{search.thumbnail}")
        await ctx.send(embed=embed)
        await vc.play(search)
        logger.info(f'Playing from YouTube: {search.title}')
    
#Play a song from SoundCloud, ex: !play Jackboy Seduction
@client.command(aliases=['Playsc', 'soundcloud', 'sc'])
@commands.has_role(DJ)
async def playsc(ctx, *, search: wavelink.SoundCloudTrack):
    vc = ctx.voice_client
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)
        await vc.set_volume(5)#initially set volume to 5

    if vc.is_playing():
        vc.queue.put(item=search)
        embed = discord.Embed(title=search.title, url=search.uri, description=f"Added {search.title} to the Queue!", colour=discord.Colour.random())
        embed.set_author(name=f"{search.author}")
        if vc.queue.is_empty:
            embed.set_footer(text="Queue is empty")
        else:
            nextitem = vc.queue.get()
            vc.queue.put_at_front(item=nextitem)
            embed.set_footer(text=f"Next song is: {nextitem}")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=search.title, url=search.uri, description=f"Now Playing {search.title}!", colour=discord.Colour.random())
        embed.set_author(name=f"{search.author}") 
        await ctx.send(embed=embed)
        await vc.play(search)
        logger.info(f'Playing from SoundCloud: {search.title}')

#Skip current song and play next, ex !playskip blinding lights the weeknd
@client.command(aliases=['Playskip', 'PlaySkip'])
@commands.has_role(DJ)
async def playskip(ctx, *, search: wavelink.YouTubeMusicTrack):
    vc = ctx.voice_client
    if vc:
        if vc.is_playing() and not vc.is_paused():
            vc.queue.put_at_front(item = search)
            await vc.seek(vc.track.length * 1000)
            await ctx.send("Playing the next song...")
            embed = discord.Embed(title=search.title, url=search.uri, description=f"Now Playing {search.title}!", colour=discord.Colour.random())
            embed.set_author(name=f"{search.author}")
            embed.set_thumbnail(url=f"{search.thumbnail}")
            await ctx.send(embed=embed)
            logger.info(f'Playskipping to: {search.title}')
        elif vc.is_paused():
            await ctx.send('The bot is currently paused, to playskip, first resume music with !resume')
        else:
            await ctx.send('The bot is not currently playing anything.')
    else:
        await ctx.send('The bot is not connected to a voice channel.')

#Skip current song, ex: !skip
@client.command(aliases=['Skip'])
@commands.has_role(DJ)
async def skip(ctx):
    vc = ctx.voice_client 
    if vc:
        if not vc.is_playing():
            return await ctx.send('There are no songs currently playing')
        if vc.queue.is_empty:
            return await vc.stop()

        await vc.seek(vc.track.length * 1000)
        search = vc.queue.get()
        vc.queue.put_at_front(item=search)
        await ctx.send(f"Skipping to next song: {search}")
        logger.info('Skipping music')
        if vc.is_paused():
            await vc.resume()
    else:
        await ctx.send('The bot is not connected to a voice channel.')

#Pause current song, ex: !pause
@client.command(aliases=['Pause'])
@commands.has_role(DJ)
async def pause(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_playing() and not vc.is_paused():
            await vc.pause()
            await ctx.send("Paused!")
            logger.info('Pausing music')
        else:
            await ctx.send("Nothing is currently playing")
    else:
        await ctx.send("The bot is not connect to a voice channel.")
        
#Resume current song, ex: !resume
@client.command(aliases=['Resume'])
@commands.has_role(DJ)
async def resume(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_paused():
            await vc.resume()
            await ctx.send("Resuming!")
            logger.info('Resuming music')
        else:
            await ctx.send("Nothing is currently paused.")
    else:
        await ctx.send("The bot is not connected to a voice channel")

#Show current playing song, ex: !nowplaying
@client.command(aliases=['Nowplaying', 'NowPlaying', 'np'])
@commands.has_role(DJ)
async def nowplaying(ctx):
    vc = ctx.voice_client
    if vc:
        try:
            track = str(vc.track)
            await ctx.send(f'Currently playing: {track}')
            logger.info(f'Current playing track: {track}')
        except:
            await ctx.send('Nothing is currently playing, add a song by using !play or !playsc')
    else:
        await ctx.send("The bot is not connected to a voice channel")

#Show whats next in the queue
@client.command(aliases=['Next', 'nextsong'])
@commands.has_role(DJ)
async def next(ctx):
    vc = ctx.voice_client
    if vc:
        try:
            search = vc.queue.get()
            vc.queue.put_at_front(item=search)
            await ctx.send(f"The next song is: {search}")
            logger.info('Printing next song in queue')
        except:    
            await ctx.send("The queue is empty, add a song by using !play or !playsc")
    else:
        await ctx.send("The bot is not connected to a voice channel")

#Seeks to specifc second in song, ex: !seek 50(seeks to 50 seconds)
@client.command(aliases=['Seek'])
@commands.has_role(DJ)
async def seek(ctx, seek = 0):
    vc = ctx.voice_client
    val = int(seek)
    if vc:
        if vc.is_playing() and not vc.is_paused():
            await vc.seek(vc.track.length * val)
            await ctx.send(f"Seeking {val} seconds.")
            logger.info(f'Song seeked for {val} seconds')
        else:
            await ctx.send("Nothing is currently playing")
    else:
        await ctx.send("The bot is not connected to a voice channel.")

#Set volume of bot, ex !volume 1(sets volume of bot to 1)
@client.command(aliases=['Volume'])
@commands.has_role(DJ)
async def volume(ctx, volume):
    vc = ctx.voice_client
    val = int(volume)
    if vc and val > 0 and val <= 100:
        await vc.set_volume(val)
        await ctx.send(f"Volume set to: {val}")
        logger.info(f'Bot volume set to: {val}')
    else:
        await ctx.send("The bot is not connected to a voice channel.")

#Prints all items in queue, ex !queue
@client.command(aliases=['Queue'])
@commands.has_role(DJ)
async def queue(ctx):
    vc = ctx.voice_client
    desc = ""
    if vc.queue.is_empty is False:
        logger.info('Embedding Queue')
        test = vc.queue.copy()
        li = list(test)
        for i in range(len(li)):
            desc += (f"{i+1}. {li[i]}")
            desc += '\n\n'

        img = discord.File("dollar.png", filename="output.png")
        embed = discord.Embed(title='Whats Queued?', description=desc, colour=discord.Colour.random())
        embed.set_thumbnail(url="attachment://output.png")
        await ctx.send(embed=embed, file=img)
    else:
        logger.info('Queue is already empty')
        await ctx.send("The queue is currently empty, add a song by using !play or !playsc")

#Clears queue, !empty
@client.command(aliases=['Empty', 'clearqueue', 'restart'])
@commands.has_role(DJ)
async def empty(ctx):
    vc = ctx.voice_client
    if vc.queue.is_empty is False:    
        vc.queue.clear()
        logger.info('Emptying queue')
        await ctx.send("All items from queue have been removed")
    else:
        logger.info('Queue is already empty')
        await ctx.send("The queue is currently empty, add a song by using !play or !playsc")

#Clear Messages from channel, ex !clear 50
@client.command(aliases=['purge', 'delete'])
@commands.has_role(ADMIN or "MOD")
async def clear(ctx, amount=None):

    if (amount is None):
        await ctx.send("You must enter a number after the !clear")
    else:
        val = int(amount)
        if(val <= 0):
            await ctx.send("You must enter a number greater than 0")
        else:
            await ctx.channel.purge(limit=val)

#Load playlist from CSV, ex !load
@client.command(aliases=['Load'])
@commands.has_role(DJ)
async def load(ctx):
    vc = ctx.voice_client
    global run
    run = True
    count = 0 

    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)
        await vc.set_volume(5)

    await ctx.send('Loading your playlist!')
    logger.info('Loading Playlist')

    data = read_csv("ex.csv")
    tracks = data['Track Name'].tolist()
    artists = data['Artist Name(s)'].tolist()
    song = list(zip(tracks, artists))
    
    while count<=75:    
        if not run:
            break
        item = random.choice(song)
        song.remove(item)
        search = await wavelink.YouTubeTrack.search(query=item[0] + " " + item[1], return_first=True)
        if vc.is_playing():
            vc.queue.put(item=search)
            embed = discord.Embed(title=search.title, url=search.uri, description=f"Added {search.title} to the Queue!", colour=discord.Colour.random())
            embed.set_author(name=f"{search.author}")
            embed.set_thumbnail(url=f"{search.thumbnail}")
            nextitem = vc.queue.get()
            vc.queue.put_at_front(item=nextitem)
            embed.set_footer(text=f"Next song is: {nextitem}")
            await ctx.send(embed=embed)
            logger.info(f'Added {search} to queue from playlist')
        elif vc.queue.is_empty:
            embed = discord.Embed(title=search.title, url=search.uri, description=f"Now Playing {search.title}!", colour=discord.Colour.random())
            embed.set_author(name=f"{search.author}")
            embed.set_thumbnail(url=f"{search.thumbnail}")
            await ctx.send(embed=embed)
            await vc.play(search)
            logger.info(f'Playing {search} from playlist')
        else:
            logger.error('Error queuing/playing from playlist')
        count += 1

    await ctx.send('Finished loading playlist')
    logger.info(f'Finished loading {count} songs into queue from playlist')

#Print lyrics of current playing song, pulls from Genius.com
@client.command(aliases=['Lyrics'])
@commands.has_role(DJ)
async def lyrics(ctx):
    vc = ctx.voice_client
    track = str(vc.track)

    if vc.is_playing():
        async with ctx.typing():
            while True:
                try:
                    logger.debug(f'Searching lyrics for {track} by {artist}')
                    song = genius.search_song(track, artist)
                    logger.info('Lyrics loaded from Genius API')
                    break
                except: 
                    logger.debug('GET request timed out, retrying...')
            if song == None:
                await ctx.send('Unable to find song lyrics, songs from playlists are less likely to return lyrics...')
            else:
                if len(song.lyrics) > 4096:
                    return await ctx.send(f"Lyrics can be found here: <{song.url}>")
                embed = discord.Embed(title=song.title, url=song.url, description=song.lyrics, colour=discord.Colour.random())
                embed.set_author(name=f"{song.artist}")
                embed.set_thumbnail(url=f"{song.header_image_thumbnail_url}")
                embed.set_footer()
                await ctx.send(embed=embed)
    else:
        await ctx.send('Nothing is currently playing, add a song by using !play or !playsc')

#Make a post of dollars latest features(ADMIN only)
@client.command()
@commands.has_role(ADMIN)
async def patch(ctx):
    desc = '''🚩Added !lyrics command, now you see current playing song's lyrics courtesy of Genius.com 
    \n\nFixes to !lyrics:\n\t -Reduced chance to timeout\n\t -Less likely to get incorrect lyrics
    \n\nFixes to !queue:\n\t -Increased speed of printing
    \n\nFixes to !load:\n\t -Hard set to 75 songs from playlist, reduces strain on GET requests from YoutubeMusic
    \n\nOther New Features:\n\t -Added ability to print latest updates\n\t -Capitalization of first letter of commands no longer matters'''

    img = discord.File("dollar.png", filename="output.png")
    
    channel = client.get_channel(1043712431265955910)
    embed = discord.Embed(title='Dollar: Latest Update', url='https://en.wikipedia.org/wiki/Dollar', description=desc, colour=0x2ecc71)
    embed.set_thumbnail(url="attachment://output.png")
    embed.set_footer(text='Please send feature requests/bugs to Cash#8915')
    await channel.send(embed=embed, file=img)

#Stop loading playlist or printing queue
@client.command()
@commands.has_role(ADMIN or 'MOD')
async def stop(ctx):
    global run
    run = False
    logger.debug('Playlist/Queue loading interrupted')
    await ctx.send('Interrupting!')

#Error Handling if unable to find song, or user isn't in a voice channel
async def play_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Unable to find track :(")
        logger.error("Unable to find track")
    else:
        await ctx.send("Please join a voice channel")
        logger.error("User not in voice channel, bot unable to join")

#Run bot
client.run(DISCORD_TOKEN)