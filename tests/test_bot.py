import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pydiscordbot.bot import addition, bot

@pytest.mark.asyncio
async def test_addition_command_flow(mock_db):
    """Verifies the addition command correctly initializes the session and starts the quiz."""
    
    # 1. Arrange
    ctx = AsyncMock()
    ctx.author = MagicMock(id = 12345)
    
    expected_question_count = 10
    expected_a_start = 1
    expected_a_end = 2
    expected_b_start = 3
    expected_b_end = 4
    
    # We mock the dependencies to see if they get called correctly
    with patch("pydiscordbot.database.create_session", return_value=1) as mock_create_session, \
         patch("pydiscordbot.generators.generate_addition_quiz") as mock_gen, \
         patch("pydiscordbot.quiz.run_quiz", new_callable=AsyncMock) as mock_run_quiz:
        
        # Setup the generator to return a dummy list
        mock_gen.return_value = [MagicMock()]

        # 2. Act
        # Simulate typing: !addition with expected values above
        await addition(ctx, num_q=expected_question_count, a_start=expected_a_start, a_end=expected_a_end, b_start=expected_b_start, b_end=expected_b_end)

        # 3. Assert
        mock_create_session.assert_called_once_with(ctx.author.id)

        mock_gen.assert_called_once_with(
            expected_question_count, 
            expected_a_start, 
            expected_a_end, 
            expected_b_start, 
            expected_b_end)
        
        mock_run_quiz.assert_awaited_once_with(
            ctx, 
            bot, 
            mock_create_session.return_value,
            mock_gen.return_value)
        
