#This music bot uses wavelink instead of FFMPEG
#Current commands:
#join, leave, play, skip, pause, resume, seek, volume, playskip, next
import discord
import secrets
import os
import wavelink
import logging

from discord.ext import commands
from dotenv import load_dotenv

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

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
handler = logging.FileHandler(filename='discord.log', encoding='utf8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Get Discord token
DISCORD_TOKEN = os.getenv("TOKEN")

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
    print(f'Node: <{node.identifier}> is ready')
    print(f'Logged in as {node.bot.user} ({node.bot.user.id})')

@client.event
async def on_wavelink_track_end(player: CustomPlayer, track: wavelink.Track, reason):
    if not player.queue.is_empty:
        next_track = player.queue.get()
        await player.play(next_track)

#Join authors voice channel
@client.command()
async def join(ctx):
    vc = ctx.voice_client
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        return await ctx.send('You must be in a voice channel for the bot to connect.')
    if not vc:
        await ctx.author.voice.channel.connect(cls=CustomPlayer())
    else:
        await ctx.send('The bot is already connected to a voice channel')

#Leave voice channel
@client.command()
async def leave(ctx):
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
    else:
        ctx.send('The bot is not connected to a voice channel.')

#Play a song, ex: !play starboy the weeknd
@client.command()
async def play(ctx, *, search: wavelink.YouTubeTrack):
    vc = ctx.voice_client
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)

    if vc.is_playing():
        vc.queue.put(item=search)
        await ctx.send(embed=discord.Embed(
            title=search.title,
            url=search.uri,
            description=f"Added {search.title} to the Queue!"
        ))
    else:
        await ctx.send(embed=discord.Embed(
            title=search.title,
            url=search.uri,
            description=f"Now Playing {search.title}!"
        ))
        await vc.play(search)
        await vc.set_volume(25)#Set bot volume initially to 25

#Skip current song and play next, ex !playskip blinding lights the weeknd
@client.command()
async def playskip(ctx, *, search: wavelink.YouTubeTrack):
    vc = ctx.voice_client
    if vc:
        if vc.is_playing():
            vc.queue.put_at_front(item = search)
            await vc.seek(vc.track.length * 1000)
            await ctx.send("Playing the next song...")
            await ctx.send(embed=discord.Embed(
                title=search.title,
                url=search.uri,
                description=f"Now Playing {search.title}!"
            ))
        else:
            await ctx.send('The bot is not currently playing anything.')
    else:
        await ctx.send('The bot is not connected to a voice channel.')

#Skip current song, ex: !skip
@client.command()
async def skip(ctx):
    vc = ctx.voice_client 
    if vc:
        if not vc.is_playing():
            return await ctx.send('There are no songs currently playing')
        if vc.queue.is_empty:
            return await vc.stop()

        await vc.seek(vc.track.length * 1000)
        await ctx.send("Skipped!")
        if vc.is_paused():
            await vc.resume()
    else:
        await ctx.send('The bot is not connected to a voice channel.')

#Pause current song, ex: !pause
@client.command()
async def pause(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_playing() and not vc.is_paused():
            await vc.pause()
            await ctx.send("Paused!")
        else:
            await ctx.send("Nothing is currently playing")
    else:
        await ctx.send("The bot is not connect to a voice channel.")
        
#Resume current song, ex: !resume
@client.command()
async def resume(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_paused():
            await vc.resume()
            await ctx.send("Resuming!")
        else:
            await ctx.send("Nothing is currently paused.")
    else:
        await ctx.send("The bot is not connected to a voice channel")

#Show whats next in the queue
@client.command()
async def next(ctx):
    vc = ctx.voice_client
    if vc:
        await ctx.send(f"The next song is: {vc.queue.get()}")
    else:
        await ctx.send("The bot is not connected to a voice channel")

#Seeks to specifc second in song, ex: !seek 50(seeks to 50 seconds)
@client.command()
async def seek(ctx, seek = 0):
    vc = ctx.voice_client
    val = int(seek)
    if vc:
        if vc.is_playing() and not vc.is_paused():
            await vc.seek(vc.track.length * val)
            await ctx.send(f"Seeking!")
        else:
            await ctx.send("Nothing is currently playing")
    else:
        await ctx.send("The bot is not connect to a voice channel.")

#Set volume of bot, ex !volume 1(sets volume of bot to 1)
@client.command()
async def volume(ctx, volume):
    vc = ctx.voice_client
    val = int(volume)
    if vc and val > 0 and val <= 100:
        await vc.set_volume(val)
        await ctx.send(f"I set my volume to {val}")
    else:
        await ctx.send("I need to be in a voice channel to set my volume.")

#Error Handling if unable to find song, or user isn't in a voice channel
async def play_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Unable to find track :(")
    else:
        await ctx.send("Please join a voice channel")

#Run bot
client.run(DISCORD_TOKEN)