import discord
from discord.ext import commands
import os
import asyncio
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
    await message.channel.send("Welcome to the CTF Challenge! Type `play` to start your first game.")

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
    # More difficult puzzle for game 1: Binary to Decimal
    await ctx.send("Game 1: Convert this binary number to decimal: `1101`.")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.strip() == "13":
            user_games[ctx.author.id] += 1
            await ctx.send("Correct! You earned a part of the flag: " + flag_parts[0])
            await play_game(ctx)  # Automatically proceed to the next game
        else:
            await ctx.send("Wrong answer! Don't give up! Try again.")
            await game_0(ctx)  # Give the user another chance
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Don't give up! Let's try that again.")
        await game_0(ctx)  # Give the user another chance

async def game_1(ctx):
    # More difficult puzzle for game 2: Base conversion
    await ctx.send("Game 2: What is the hexadecimal representation of the decimal number 255?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.strip().lower() == "ff":
            user_games[ctx.author.id] += 1
            await ctx.send("Correct! You earned a part of the flag: " + flag_parts[1])
            await play_game(ctx)  # Automatically proceed to the next game
        else:
            await ctx.send("Wrong answer! Don't give up! Try again.")
            await game_1(ctx)  # Give the user another chance
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Don't give up! Let's try that again.")
        await game_1(ctx)  # Give the user another chance

async def game_2(ctx):
    # Riddle for game 3
    await ctx.send("Game 3: Solve the riddle: I speak without a mouth and hear without ears. What am I?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.strip().lower() == "echo":
            user_games[ctx.author.id] += 1
            await ctx.send("Correct! You earned a part of the flag: " + flag_parts[2])
            await play_game(ctx)  # Automatically proceed to the next game
        else:
            await ctx.send("Wrong answer! Don't give up! Try again.")
            await game_2(ctx)  # Give the user another chance
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Don't give up! Let's try that again.")
        await game_2(ctx)  # Give the user another chance

async def game_3(ctx):
    # Riddle for game 4
    await ctx.send("Game 4: What comes once in a minute, twice in a moment, but never in a thousand years?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.strip().lower() == "the letter m":
            user_games[ctx.author.id] += 1
            await ctx.send("Correct! You earned a part of the flag: " + flag_parts[3])
            await ctx.send("Congratulations! You've completed all the games! Here's your full flag: " + "".join(flag_parts))
        else:
            await ctx.send("Wrong answer! Don't give up! Try again.")
            await game_3(ctx)  # Give the user another chance
    except asyncio.TimeoutError:
        await ctx.send("Time's up! Don't give up! Let's try that again.")
        await game_3(ctx)  # Give the user another chance

keep_alive()
bot.run(token)
