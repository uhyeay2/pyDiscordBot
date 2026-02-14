import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pydiscordbot.quiz import run_quiz
from pydiscordbot.models import QuizQuestion

@pytest.mark.asyncio
async def test_run_quiz_success(mock_db):
    """Tests the full flow of a correctly answered question."""
    # 1. Setup Mocks
    ctx = AsyncMock()
    bot = AsyncMock()
    
    # Fake a Discord message response
    mock_msg = MagicMock()
    mock_msg.content = "A"
    mock_msg.author = ctx.author
    mock_msg.channel = ctx.channel
    
    # bot.wait_for is a coroutine, so it needs AsyncMock
    bot.wait_for = AsyncMock(return_value=mock_msg)
    
    # 2. Setup Data
    questions = [
        QuizQuestion(
            question_text="What is 2+2?", 
            correct_answer="4", 
            options=["4", "5"] 
        )
    ]

    # 3. Act
    # We patch random.shuffle so '4' (the correct answer) stays at index 0 (Letter A)
    with patch("random.shuffle", lambda x: None):
        await run_quiz(ctx, bot, session_id=1, questions=questions)

    # 4. Assert
    # Verify Discord was "notified"
    ctx.send.assert_any_call(f"🚀 Starting quiz session #1! Get ready...")
    
    # Verify Database recorded the truth
    cursor = mock_db.cursor()
    cursor.execute("SELECT user_answer, is_correct FROM questions_results")
    row = cursor.fetchone()
    assert row["user_answer"] == "4"
    assert row["is_correct"] == 1 

@pytest.mark.asyncio
async def test_run_quiz_timeout(mock_db):
    """Tests that the system handles a user not responding."""
    ctx = AsyncMock()
    bot = AsyncMock()
    
    # Force a timeout
    bot.wait_for = AsyncMock(side_effect=asyncio.TimeoutError)
    
    questions = [QuizQuestion("Fast?", "Yes", ["No"])]

    await run_quiz(ctx, bot, session_id=99, questions=questions)

    # Verify DB recorded the timeout
    cursor = mock_db.cursor()
    cursor.execute("SELECT user_answer, is_correct, response_time_ms FROM questions_results")
    row = cursor.fetchone()
    assert row["user_answer"] == "TIMEOUT"
    assert row["is_correct"] == 0
    assert row["response_time_ms"] == 15000.0  # Our hardcoded timeout penalty