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
flag_parts = [os.environ[f"part{i}"] for i in range(1, 11)]
answers = [os.environ[f"answer{i}"] for i in range(1, 11)]
game_names = [os.environ[f"game_name{i}"] for i in range(1, 11)]
user_games = {}  # To track user progress
completed_games = {}  # Track completed games for users

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
        await show_game_list(message)

    await bot.process_commands(message)

async def show_game_list(message):
    user_id = message.author.id
    if user_id in user_games:
        await message.channel.send("You're already in a game! Type `!change` to switch games or answer the current one.")
        return

    user_games[user_id] = []  # Initialize the user's game state
    game_list = "\n".join(f"{i + 1}: {game_names[i]}" for i in range(len(game_names)))
    await message.channel.send(f"Welcome to the CTF Challenge! Here are the available games:\n{game_list}\nType the game number to start.")

@bot.command(name='change')
async def change_game(ctx):
    user_id = ctx.author.id
    if user_id not in user_games:
        await ctx.send("Please start the game by typing `start` first!")
        return
    
    await show_game_list(ctx.message)

@bot.event
async def on_message(message):
    user_id = message.author.id
    if message.author == bot.user:
        return

    if user_id in user_games and isinstance(user_games[user_id], list):
        try:
            game_number = int(message.content.strip()) - 1
            if 0 <= game_number < len(game_names):
                if game_number in completed_games.get(user_id, []):
                    await message.channel.send("You've already completed this game! Choose another one.")
                else:
                    await globals()[f'game_{game_number}'](message)
            else:
                await message.channel.send("Please enter a valid game number from the list.")
        except ValueError:
            if message.content.lower() == "change":
                await change_game(message)
            else:
                await message.channel.send("Invalid input. Please enter a game number or type `change`.")

async def game_0(message):
    await message.channel.send("Game 1: Convert this binary number to decimal: `1101`.")
    await wait_for_answer(message, 0)

async def game_1(message):
    await message.channel.send("Game 2: What is the hexadecimal representation of the decimal number 255?")
    await wait_for_answer(message, 1)

async def game_2(message):
    await message.channel.send("Game 3: Solve the riddle: I speak without a mouth and hear without ears. What am I?")
    await wait_for_answer(message, 2)

async def game_3(message):
    await message.channel.send("Game 4: What comes once in a minute, twice in a moment, but never in a thousand years?")
    await wait_for_answer(message, 3)

# Add more game functions as needed...
# Example for games 4-9:
async def game_4(message):
    await message.channel.send("Game 5: What is the capital of France?")
    await wait_for_answer(message, 4)

# This should include your existing game logic for games 5 through 9.

async def wait_for_answer(message, game_index):
    user_id = message.author.id

    def check(m):
        return m.author == message.author and m.channel == message.channel

    try:
        msg = await bot.wait_for('message', check=check)
        if msg.content.strip().lower() == answers[game_index]:
            if user_id not in completed_games:
                completed_games[user_id] = []
            completed_games[user_id].append(game_index)
            await message.channel.send("Correct! You earned a part of the flag: " + flag_parts[game_index])
            await show_game_list(message)  # Show the game list again after winning
        else:
            await message.channel.send("Wrong answer! " + random.choice(supportive_messages))
            await wait_for_answer(message, game_index)  # Wait for another answer
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}")

keep_alive()
bot.run(token)
