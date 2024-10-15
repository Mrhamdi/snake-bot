import discord
from discord.ext import commands
import os
import random
from keep_alive import keep_alive

token = os.environ["token"]
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Game variables
flag_parts = [os.environ[f"part{i}"] for i in range(1, 5)]
answers = [os.environ[f"answer{i}"] for i in range(1, 5)]
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
    if user_id in user_games:
        await message.channel.send("You're already in a game! Type `!play` to continue.")
        return

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
        await globals()[f'game_{game_number}'](ctx)
    else:
        await ctx.send("You've completed all the games! Here's your flag: " + "".join(flag_parts))
        await ctx.send("Thank you for playing! Type `start` to play again.")
        del user_games[user_id]  # Reset user game progress

async def game_0(ctx):
    await ctx.send("Game 1: Convert this binary number to decimal: `1101`.")
    await wait_for_answer(ctx, 0)

async def game_1(ctx):
    await ctx.send("Game 2: What is the hexadecimal representation of the decimal number 255?")
    await wait_for_answer(ctx, 1)

async def game_2(ctx):
    await ctx.send("Game 3: Solve the riddle: I speak without a mouth and hear without ears. What am I?")
    await wait_for_answer(ctx, 2)

async def game_3(ctx):
    await ctx.send("Game 4: What comes once in a minute, twice in a moment, but never in a thousand years?")
    await wait_for_answer(ctx, 3)

async def wait_for_answer(ctx, game_index):
    user_id = ctx.author.id

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        try:
            msg = await bot.wait_for('message', check=check)
            if msg.content.strip().lower() == answers[game_index]:
                user_games[user_id] += 1
                await ctx.send("Correct! You earned a part of the flag: " + flag_parts[game_index])
                await play_game(ctx)  # Automatically proceed to the next game
                break
            else:
                await ctx.send("Wrong answer! " + random.choice(supportive_messages))
        except discord.Forbidden:
            await ctx.send("I can't send messages in this channel.")
            break
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")
            break

keep_alive()
bot.run(token)
