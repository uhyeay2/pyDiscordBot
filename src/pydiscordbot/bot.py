import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from . import database, generators, quiz

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    database.initialize_db()
    print(f'✅ {bot.user} is online and database is initialized.')

@bot.command()
async def addition(ctx: commands.Context, num_q: int = 5, a_start: int = 1, a_end: int = 20, b_start: int = 1, b_end: int = 20):
    """
    Starts an addition quiz. 
    Usage: !addition [questions] [range_min] [range_max]
    Example: !addition 10 1 100
    """
    # 1. Create a session in the DB
    # Note: In a real app, you might want a 'math' group_id or name
    session_id = database.create_session(ctx.author.id)
    
    # 2. Generate the questions using our custom ranges
    questions = generators.generate_addition_quiz(num_q, a_start, a_end, b_start, b_end)
    
    # 3. Hand off to the generic quiz engine
    await quiz.run_quiz(ctx, bot, session_id, questions)

def run():
    bot.run(TOKEN)