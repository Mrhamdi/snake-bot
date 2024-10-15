import discord
from discord.ext import commands
import os

token = os.environ["token"]
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "hello":
        await message.channel.send(f"Hello, {message.author.name}! How can I help you today?")
    elif message.content.lower() == "start":
        await message.channel.send("Welcome! Type `!commands` for available commands.")
    
    await bot.process_commands(message)

@bot.command(name='commands')
async def commands_list(ctx):
    await ctx.send("Available commands:\n`hello` - Greet the bot\n`start` - Get a welcome message")

bot.run(token)
