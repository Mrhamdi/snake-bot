import discord
from discord.ext import commands
import os
import random
from keep_alive import keep_alive

token = os.environ["token"]
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
part1= os.environ["part1"]
part2= os.environ["part2"]
part3= os.environ["part3"]
part4= os.environ["part4"]

answer1= os.environ["answer1"]
answer2= os.environ["answer2"]
answer3= os.environ["answer3"]
answer4= os.environ["answer4"]


# Flag parts for the games
flag_parts = [part1,part2,part3,part4]
user_games = {}  # To track user progress

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
        await ctx.send("Thank you for playing! Type `start` to play again.")

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
        await ctx.send("Wrong answer! " + random.choice(supportive_messages))
        await game_0(ctx)  # Give the user another chance

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
        await ctx.send("Wrong answer! " + random.choice(supportive_messages))
        await game_1(ctx)  # Give the user another chance

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
        await ctx.send("Wrong answer! " + random.choice(supportive_messages))
        await game_2(ctx)  # Give the user another chance

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
        await ctx.send("Wrong answer! " + random.choice(supportive_messages))
        await game_3(ctx)  # Give the user another chance

keep_alive()
bot.run(token)
