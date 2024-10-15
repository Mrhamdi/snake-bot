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
flag_parts = [
    os.environ["part1"],
    os.environ["part2"],
    os.environ["part3"],
    os.environ["part4"],
    os.environ["part5"],
    os.environ["part6"],
    os.environ["part7"],
    os.environ["part8"],
    os.environ["part9"],
    os.environ["part10"]
]

answers = [
    os.environ["answer1"],  # Binary to decimal
    os.environ["answer2"],  # Hexadecimal of 255
    os.environ["answer3"],  # Riddle
    os.environ["answer4"],  # Riddle
    os.environ["answer5"],  # Riddle: What has keys but can't open locks?
    os.environ["answer6"],  # Cryptography: Reverse "dlrow olleh"
    os.environ["answer7"],  # Riddle: What has a heart that doesn't beat?
    os.environ["answer8"],  # Cryptography: Caesar cipher for "hello"
    os.environ["answer9"],  # Riddle: What runs but never walks?
    os.environ["answer10"]   # Simple math: What is 5 + 3?
]

game_names = [
    "Binary to Decimal Conversion",
    "Hexadecimal Conversion",
    "Riddle: Speak Without a Mouth",
    "Riddle: Once in a Minute",
    "Riddle: Keys But No Locks",
    "Cryptography: Reverse a String",
    "Riddle: Heart That Doesn't Beat",
    "Cryptography: Caesar Cipher",
    "Riddle: Runs but Never Walks",
    "Math Question: Simple Addition"
]

user_games = {}
completed_games = {}

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

    user_games[user_id] = []
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

async def game_4(message):
    await message.channel.send("Game 5: What has keys but can't open locks?")
    await wait_for_answer(message, 4)

async def game_5(message):
    await message.channel.send("Game 6: Reverse the following string: `dlrow olleh`.")
    await wait_for_answer(message, 5)

async def game_6(message):
    await message.channel.send("Game 7: What has a heart that doesn't beat?")
    await wait_for_answer(message, 6)

async def game_7(message):
    await message.channel.send("Game 8: What is 'khoor' when shifted by 3 letters (Caesar cipher)?")
    await wait_for_answer(message, 7)

async def game_8(message):
    await message.channel.send("Game 9: What runs but never walks?")
    await wait_for_answer(message, 8)

async def game_9(message):
    await message.channel.send("Game 10: What is 5 + 3?")
    await wait_for_answer(message, 9)

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
            await show_game_list(message)
        else:
            await message.channel.send("Wrong answer! " + random.choice(supportive_messages))
            await wait_for_answer(message, game_index)
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}")

keep_alive()
bot.run(token)
