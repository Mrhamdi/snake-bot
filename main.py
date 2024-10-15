import discord
from discord.ext import commands
import os
import random

# Initialize the bot
token = os.environ["token"]
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Game data
games = {
    1: ("Convert this binary number to decimal: `1101`.", "13"),
    2: ("What is the hexadecimal representation of the decimal number 255?", "ff"),
    3: ("I speak without a mouth and hear without ears. What am I?", "an echo"),
    4: ("What comes once in a minute, twice in a moment, but never in a thousand years?", "the letter m"),
    5: ("What has keys but can't open locks?", "a piano"),
    6: ("Reverse this: `dlrow olleh`.", "hello world"),
    7: ("What has a heart that doesn't beat?", "an artichoke"),
    8: ("Decrypt this Caesar cipher: `khoor` (shift by 3).", "hello"),
    9: ("What runs but never walks?", "a river"),
    10: ("What is 5 + 3?", "8"),
}

user_games = {}
completed_games = {}

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "start":
        await show_game_list(message)
    else:
        await bot.process_commands(message)

async def show_game_list(message):
    user_id = message.author.id
    if user_id in user_games:
        await message.channel.send("You're already in a game! Type `!change` to switch games.")
        return

    user_games[user_id] = []
    game_list = "\n".join(f"{i}: {desc[0]}" for i, desc in games.items())
    await message.channel.send(f"Welcome! Here are the available games:\n{game_list}\nType the game number to start.")

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

    if user_id in user_games:
        try:
            game_number = int(message.content.strip())
            if game_number in games and game_number not in completed_games.get(user_id, []):
                await start_game(message, game_number)
            else:
                await message.channel.send("Invalid game number or you have already completed this game.")
        except ValueError:
            if message.content.lower() == "change":
                await change_game(message)

async def start_game(message, game_number):
    question, correct_answer = games[game_number]
    await message.channel.send(f"Game {game_number}: {question}")

    def check(m):
        return m.author == message.author and m.channel == message.channel

    try:
        msg = await bot.wait_for('message', check=check)
        if msg.content.strip().lower() == correct_answer:
            if message.author.id not in completed_games:
                completed_games[message.author.id] = []
            completed_games[message.author.id].append(game_number)
            await message.channel.send("Correct! Type `!change` to select another game.")
        else:
            await message.channel.send("Wrong answer! Try again.")
            await start_game(message, game_number)  # Allow retry
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}")

bot.run(token)
