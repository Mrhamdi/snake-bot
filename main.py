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
        await message.channel.send("Welcome! Type `!help` for commands.")
    
    await bot.process_commands(message)

@bot.command(name='help')
async def help_command(ctx):
    await ctx.send("Available commands:\n`hello` - Greet the bot\n`start` - Get a welcome message")

keep_alive()  # If you're using a keep_alive function to keep the bot running
bot.run(token)
