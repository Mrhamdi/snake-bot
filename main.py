import discord
from discord.ext import commands
import os
import random
from keep_alive import keep_alive

token = os.environ["token"]
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

part1 = os.environ["part1"]
part2 = os.environ["part2"]
part3 = os.environ["part3"]
part4 = os.environ["part4"]

answer1 = os.environ["answer1"]
answer2 = os.environ["answer2"]
answer3 = os.environ["answer3"]
answer4 = os.environ["answer4"]

# Flag parts for the games
flag_parts = [part1, part2, part3, part4]
user_games = {}  # To track user progress
active_games = {}  # To track if a user is in an active game

# Supportive messages
supportive_messages = [
    "Keep on keeping on!",
    "Good luck today! I know you’ll do great.",
    "You got this.",
    "The expert at anything was once a beginner."
]

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}!')
    # Reset user progress on server restart
    global user_games, active_games
    user_games = {}
    active_games = {}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "start":
        await start_game(message)

    await bot.process_commands(message)

async def start_game(message):
    user_id = message.author.id
    if user_id in active_games:
        await message.channel.send("You are already in a game! Please finish the current game first.")
        return

    user_games[user_id] = 0  # Start at game 0
    active_games[user_id] = True  # Mark user as active in a game
    await message.channel.send(f"Welcome to the CTF Challenge, {message.author.name}! Type `!play` to start your first game.")

@bot.command(name='play')
async def play_game(ctx):
    user_id = ctx.author.id

    if user_id not in user_games:
        await ctx.send("Please start the game by typing `start` first!")
        return

    if user_id in active_games:
        await ctx.send("You are already in a game! Please finish the current game first.")
        return

    game_number = user_games[user_id]

    if game_number < len(flag_parts):
        # Call the respective game function
        await globals()[f'game_{game_number}'](ctx)
    else:
        await ctx.send("You have completed all the games! Here's your flag: " + "".join(flag_parts))
        await ctx.send("Thank you for playing! Type `start` to play again.")
        del active_games[user_id]  # Mark user as inactive

@bot.command(name='exit')
async def exit_game(ctx):
    user_id = ctx.author.id
    if user_id in active_games:
        del active_games[user_id]  # Remove user from active games
        del user_games[user_id]  # Reset user progress
        await ctx.send("You have exited the game. You can now type `start` to play again.")
    else:
        await ctx.send("You are not currently in a game.")

async def game_0(ctx):
    await ctx.send("Game 1: Convert this binary number to decimal: `1101`.")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await bot.wait_for('message', check=check)
    if msg.content.strip() == answer1:
        user_games[ctx.author.id] += 1
        await ctx.send("Correct! You earned a part of the flag: " + flag_parts[0])
        await play_game(ctx)  # Automatically proceed to the next game
    else:
        await ctx.send("Wrong answer! The correct answer was: " + answer1)
        user_games[ctx.author.id] += 1  # Move to next game despite failure
        await play_game(ctx)  # Move on to the next game

async def game_1(ctx):
    await ctx.send("Game 2: What is the hexadecimal representation of the decimal number 255?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await bot.wait_for('message', check=check)
    if msg.content.strip().lower() == answer2:
        user_games[ctx.author.id] += 1
        await ctx.send("Correct! You earned a part of the flag: " + flag_parts[1])
        await play_game(ctx)  # Automatically proceed to the next game
    else:
        await ctx.send("Wrong answer! The correct answer was: " + answer2)
        user_games[ctx.author.id] += 1  # Move to next game despite failure
        await play_game(ctx)  # Move on to the next game

async def game_2(ctx):
    await ctx.send("Game 3: Solve the riddle: I speak without a mouth and hear without ears. What am I?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await bot.wait_for('message', check=check)
    if msg.content.strip().lower() == answer3:
        user_games[ctx.author.id] += 1
        await ctx.send("Correct! You earned a part of the flag: " + flag_parts[2])
        await play_game(ctx)  # Automatically proceed to the next game
    else:
        await ctx.send("Wrong answer! The correct answer was: " + answer3)
        user_games[ctx.author.id] += 1  # Move to next game despite failure
        await play_game(ctx)  # Move on to the next game

async def game_3(ctx):
    await ctx.send("Game 4: What comes once in a minute, twice in a moment, but never in a thousand years?")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await bot.wait_for('message', check=check)
    if msg.content.strip().lower() == answer4:
        user_games[ctx.author.id] += 1
        await ctx.send("Correct! You earned a part of the flag: " + flag_parts[3])
        await ctx.send("Congratulations! You've completed all the games! Here's your full flag: " + "".join(flag_parts))
        await ctx.send("Thank you for playing! Type `start` to play again.")
    else:
        await ctx.send("Wrong answer! The correct answer was: " + answer4)
        await ctx.send("Thank you for playing! Type `start` to play again.")

    del active_games[ctx.author.id]  # Mark user as inactive

keep_alive()
bot.run(token)
