import discord
from discord.ext import commands
import os
import random

token = os.environ["token"]
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Simple CTF challenges
challenges = {
    "What is 2 + 2?": "4",
    "What is the capital of France?": "paris",
    "What is the color of the sky on a clear day?": "blue",
    "What do you call a group of wolves?": "pack",
}

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "start":
        await message.channel.send(f"Hello, {message.author.name}! Type `!commands` for available commands.")
    
    await bot.process_commands(message)

@bot.command(name='commands')
async def commands_list(ctx):
    await ctx.send("Available commands:\n`!hello` - Greet the bot\n`!start` - Welcome message\n`!challenge` - Start a CTF challenge")

@bot.command(name='hello')
async def greet(ctx):
    await ctx.send(f"Hello, {ctx.author.name}!")

@bot.command(name='challenge')
async def challenge(ctx):
    question, answer = random.choice(list(challenges.items()))
    await ctx.send(f"Challenge: {question}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30)  # Wait for an answer
        if msg.content.strip().lower() == answer:
            await ctx.send("Correct! You've earned a point!")
        else:
            await ctx.send(f"Wrong! The correct answer was: {answer}")
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long! The correct answer was: {answer}")

bot.run(token)
