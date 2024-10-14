import discord
from discord.ext import commands
import os
import random
from keep_alive import keep_alive

token = os.environ["token"]
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Flag parts for the games
flag_parts = [
    "Sicca{go4_",
    "d1fficu1t_",
    "g4m3s_ar3_",
    "fun_and_3asy}"
]
user_games = {}  # To track user progress

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "start":
        await start_game(message)

    await bot.process_commands(message)

async def start_game(message):
    user_id = message.author.id
    user_games[user_id] = 0  # Start at game 0
    await message.channel.send("Welcome to the CTF Challenge! Type `!play` to start your first game.")

@bot.command(name='play')
async def play_game(ctx):
    user_id = ctx.author.id

    if user_id not in user_games:
        await ctx.send("Please start the game by typing `start` first!")
        return

    game_number = user_games[user_id]

    if game_number < len(flag_parts):
        # Call the respective game function
        await globals()[f'game_{game_number}'](ctx)
    else:
        await ctx.send("You have completed all the games! Here's your flag: " + "".join(flag_parts))

async def game_0(ctx):
    # Example puzzle for game 1
    await ctx.send("Game 1: What is 5 + 3?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content == "8":
            user_games[ctx.author.id] += 1
            await ctx.send("Correct! You earned a part of the flag: " + flag_parts[0])
        else:
            await ctx.send("Wrong answer! Game over.")
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Game over.")

async def game_1(ctx):
    # Example puzzle for game 2
    await ctx.send("Game 2: What is the capital of France?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.lower() == "paris":
            user_games[ctx.author.id] += 1
            await ctx.send("Correct! You earned a part of the flag: " + flag_parts[1])
        else:
            await ctx.send("Wrong answer! Game over.")
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Game over.")

async def game_2(ctx):
    # Example puzzle for game 3
    await ctx.send("Game 3: Solve the riddle: I speak without a mouth and hear without ears. What am I?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.lower() == "echo":
            user_games[ctx.author.id] += 1
            await ctx.send("Correct! You earned a part of the flag: " + flag_parts[2])
        else:
            await ctx.send("Wrong answer! Game over.")
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Game over.")

async def game_3(ctx):
    # Example puzzle for game 4
    await ctx.send("Game 4: What comes once in a minute, twice in a moment, but never in a thousand years?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.lower() == "the letter m":
            user_games[ctx.author.id] += 1
            await ctx.send("Correct! You earned a part of the flag: " + flag_parts[3])
        else:
            await ctx.send("Wrong answer! Game over.")
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Game over.")

keep_alive()
bot.run(token)


