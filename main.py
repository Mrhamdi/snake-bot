import discord
from discord.ext import commands
from keep_alive import keep_alive
import os 



token = os.environ["token"]
part1 = os.environ["part1"]
part2= os.environ["part2"]
part3 = os.environ["part3"]
part4 = os.environ["part4"]
part5 = os.environ["part5"]
part6= os.environ["part6"]
part7= os.environ["part7"]
part8= os.environ["part8"]
part9= os.environ["part9"]
part10= os.environ["part10"]
flag= os.environ["flag"]
answer1 = os.environ["answer1"]
answer2= os.environ["answer2"]
answer3 = os.environ["answer3"]
answer4 = os.environ["answer4"]
answer5 = os.environ["answer5"]
answer6= os.environ["answer6"]
answer7= os.environ["answer7"]
answer8= os.environ["answer8"]
answer9= os.environ["answer9"]
answer10= os.environ["answer10"]


intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

player_res = {}
completed_games = {}
incorrect_attempts = {}
flags = [
    part1, part2, part3, 
    part4, part5,part6, 
    part7, part8,part9, 
    part10
]
total_games = len(flags)

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id

    if message.content.lower() == "start":
        if user_id in player_res:
            await message.channel.send("You are already in a game! Please finish the current game first.")
        else:
            player_res[user_id] = None
            completed_games[user_id] = set()
            incorrect_attempts[user_id] = {}
            await show_games(message, user_id)

    await bot.process_commands(message)

async def show_games(message, user_id):
    game_list = [
        "1: Game 1 - Bin10",
        "2: Game 2 - HexMe255",
        "3: Game 3 - RiddleOfVoice",
        "4: Game 4 - KeyRiddle",
        "5: Game 5 - KeyMystery",
        "6: Game 6 - SweetReverse",
        "7: Game 7 - FileLister",
        "8: Game 8 - Colosseum",
        "9: Game 9 - BranchMystery",
       "10: Game 10 - TEnigma"
    ]

    formatted_games = []
    for index, game in enumerate(game_list, start=1):
        if index in completed_games[user_id]:
            formatted_games.append(f"~~{game}~~")
        else:
            formatted_games.append(game)

    await message.channel.send("Nice, let's start! Here are the available games:\n" + "\n".join(formatted_games))
    await message.channel.send("Please type the number of the game you want to play!")

    while True:
        def check(m):
            return m.author == message.author and m.channel == message.channel

        msg = await bot.wait_for('message', check=check)

        if msg.content.isdigit() and int(msg.content) in range(1, total_games + 1):
            game_number = int(msg.content)
            if game_number in completed_games[user_id]:
                await message.channel.send("You've already completed this game! Please choose another.")
                continue
            else:
                player_res[user_id] = game_number
                incorrect_attempts[user_id][game_number] = 0
                await play_game(message, user_id)
                break
        else:
            await message.channel.send("Invalid choice! Please choose a valid game number.")

async def play_game(message, user_id):
    game_number = player_res[user_id]
    
    if game_number == 1:
        await game_0(message, user_id)
    elif game_number == 2:
        await game_1(message, user_id)
    elif game_number == 3:
        await game_2(message, user_id)
    elif game_number == 4:
        await game_3(message, user_id)
    elif game_number == 5:
        await game_4(message, user_id)
    elif game_number == 6:
        await game_5(message, user_id)
    elif game_number == 7:
        await game_6(message, user_id)
    elif game_number == 8:
        await game_7(message, user_id)
    elif game_number == 9:
        await game_8(message, user_id)
    elif game_number == 10:
        await game_9(message, user_id)
    else:
        await message.channel.send("Something went wrong. Please start again with `start`.")

async def game_0(message, user_id):
    await message.channel.send("Game 1: Bin10")
    await play_game_logic(message, user_id, answer1, 1)

async def game_1(message, user_id):
    await message.channel.send("Game 2:HexMe 255")
    await play_game_logic(message, user_id, answer2, 2)

async def game_2(message, user_id):
    await message.channel.send("Game 3:I speak without a mouth and hear without ears. What am I?")
    await play_game_logic(message, user_id, answer3, 3)

async def game_3(message, user_id):
    await message.channel.send("Game 4: What has keys but can't open locks?")
    await play_game_logic(message, user_id, answer4, 4)

async def game_4(message, user_id):
    await message.channel.send("Game 5: What is the key for the lock if '4' means 'D', '1' means 'A', '3' means 'C'?")
    await play_game_logic(message, user_id, answer5, 5)

async def game_5(message, user_id):
    await message.channel.send("Game 6: Reverse this string: 'dlroW olleH'")
    await play_game_logic(message, user_id, answer6, 6)

async def game_6(message, user_id):
    await message.channel.send("Game 7: List all files in a directory using linux command")
    await play_game_logic(message, user_id, answer7, 7)

async def game_7(message, user_id):
    await message.channel.send("Game 8: Decode: 'Dg qhg vc qh'")
    await play_game_logic(message, user_id, answer8, 8)

async def game_8(message, user_id):
    await message.channel.send("Game 9:I have branches, but no leaves, no trunk, and no fruit. What am I?")
    await play_game_logic(message, user_id, answer9, 9)

async def game_9(message, user_id):
    await message.channel.send("Game 10: What begins with T, ends with T, and has T in it?")
    await play_game_logic(message, user_id, answer10, 10)

async def play_game_logic(message, user_id, correct_answer, game_number):
    def check(m):
        return m.author == message.author and m.channel == message.channel

    while True:
        msg = await bot.wait_for('message', check=check)
        if msg.content.strip().lower() == correct_answer.lower():  
            await message.channel.send(f"Correct! You earned: {flags[game_number - 1]}")
            completed_games[user_id].add(game_number)
            incorrect_attempts[user_id][game_number] = 0
            await check_completion(message, user_id)
            await show_games(message, user_id)
            break
        else:
            if game_number not in incorrect_attempts[user_id]:
                incorrect_attempts[user_id][game_number] = 0
            incorrect_attempts[user_id][game_number] += 1
            await message.channel.send("Wrong answer! Try again.")
            if await check_attempts(message, user_id, game_number):
                break

async def check_attempts(message, user_id, game_number):
    if incorrect_attempts[user_id][game_number] >= 3:
        await message.channel.send("You've reached the maximum number of incorrect attempts for this game. You can choose a new game!")
        await show_games(message, user_id)
        return True
    return False

first_blood_sent = False  

async def check_completion(message, user_id):
    global first_blood_sent  

    if len(completed_games[user_id]) == total_games:
        
        if not first_blood_sent:
            await notify_first_blood(message.author.name)  
            first_blood_sent = True  

        await message.channel.send(f"Congratulations, {message.author.name}! Your flag is: `sicca{{dkdnjdnj}}`")


async def notify_first_blood(player_name):
    channel = bot.get_channel(1296056974097649734)
    if channel:
        await channel.send(f"🏆 First Blood! Congratulations to {player_name} for completing all games first!")

keep_alive()
bot.run(token)
