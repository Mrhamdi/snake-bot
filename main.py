import discord
from discord.ext import commands
import os 
from keep_alive import keep_alive

token=os.environ["token"]
intents = discord.Intents.default()
intents.messages = True  # Make sure to enable message intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself to prevent loops
    if message.author == bot.user:
        return
    
    if message.content.lower() == "start":
        await message.channel.send("Hi")

    if message.content.lower() == "flag":
        await message.channel.send("Hi")

    # This is necessary to allow commands to be processed as well
    await bot.process_commands(message)

# Registering the slash command
@bot.tree.command(name="snake", description="Start a snake game")
async def snake(interaction: discord.Interaction):
    await interaction.response.send_message("Snake game started! 🐍")

# Run the bot
keep_alive()
bot.run(token)

