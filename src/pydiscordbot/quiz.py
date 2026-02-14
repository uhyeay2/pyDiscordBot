import time
import asyncio
import random
from .models import QuestionResult, QuizQuestion
from typing import List
from discord.ext import commands
from . import database

async def run_quiz(ctx: commands.Context, bot: commands.Bot, session_id: int, questions: List[QuizQuestion]) -> None:
    """A generic quiz engine that handles any list of QuizQuestion objects."""
    
    await ctx.send(f"🚀 Starting quiz session #{session_id}! Get ready...")
    
    score = 0

    for q in questions:
        # 1. Present Question
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']  
        
        random.shuffle(q.options)
        option_map = dict(zip(letters, q.options))
        
        display_text = f"**{q.question_text}**\n"
        display_text += "\n".join([f"**{k})** {v}" for k, v in option_map.items()])
        
        await ctx.send(display_text)
        
        # 2. Start Timer
        start_perf = time.perf_counter()
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.upper() in letters

        try:
            msg = await bot.wait_for('message', check=check, timeout=15.0)
            end_perf = time.perf_counter()
            
            # 3. Process Result
            duration_ms = (end_perf - start_perf) * 1000
            user_choice = msg.content.upper()
            user_answer_text = option_map.get(user_choice)
            is_correct = user_answer_text == q.correct_answer
            score += 1 if is_correct else 0

            database.save_result(QuestionResult(
                id=None,
                quiz_sessions_id = session_id,
                question_text = q.question_text,
                user_answer = user_answer_text,
                correct_answer = q.correct_answer,
                is_correct = is_correct,
                response_time_ms=duration_ms
            ))
            
            feedback = "✅ Correct!" if is_correct else f"❌ Wrong! The correct answer was **{q.correct_answer}**."
            await ctx.send(f"{feedback} ({duration_ms:.2f}ms)")
            
        except asyncio.TimeoutError:
            database.save_result(QuestionResult(
                id=None,
                quiz_sessions_id = session_id,
                question_text = q.question_text,
                user_answer = "TIMEOUT",
                correct_answer = q.correct_answer,
                is_correct = False,
                response_time_ms=15000.0
            ))
            await ctx.send("⏰ Time's up! Moving to next question...")

    # 4. Wrap up session
    avg_score = database.finalize_session(session_id)
    await ctx.send(f"🏁 Quiz Complete!\nScore: {score}/{len(questions)}\nYour average response time: **{avg_score}ms**.")