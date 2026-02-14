import pytest
from pydiscordbot.models import QuestionResult, QuizSession
import pydiscordbot.database as db

@pytest.mark.parametrize("table_name", [
    "question_groups", 
    "questions", 
    "quiz_sessions", 
    "questions_results"
])

def test_initialize_db(mock_db, table_name: str) -> None:    
    cursor = mock_db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name = ?;", (table_name,))
    row = cursor.fetchone()
    assert row is not None
    assert row["name"] == table_name

def test_create_session(mock_db) -> None:
    user_id = 12345
    question_groups_id = 1
    session_id = db.create_session(user_id, question_groups_id)
    assert session_id is not None
    
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM quiz_sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    result: QuizSession = QuizSession(**dict(row)) if row else None

    assert result is not None
    assert result.id == session_id
    assert result.user_id == user_id
    assert result.question_groups_id == question_groups_id
    assert result.started_at is not None
    assert result.ended_at is None    

def test_save_result(mock_db) -> None:
    # Arrange
    questionResult: QuestionResult = QuestionResult(
        id=None,  # This will be auto-incremented by the DB
        quiz_sessions_id=1,
        question_text="What is 2+2?",
        user_answer="4",
        correct_answer="4",
        is_correct=True,
        response_time_ms=123.45
    )
    # Act
    db.save_result(questionResult)
    # Assert
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM questions_results WHERE quiz_sessions_id = ?", (1,))
    row = cursor.fetchone()
    result: QuestionResult = QuestionResult(**dict(row)) if row else None
    assert result is not None
    assert result.id is not None
    assert result.quiz_sessions_id == questionResult.quiz_sessions_id
    assert result.question_text == questionResult.question_text
    assert result.correct_answer == questionResult.correct_answer
    assert result.user_answer == questionResult.user_answer  
    assert result.is_correct == 1 if questionResult.is_correct else 0
    assert result.response_time_ms == questionResult.response_time_ms

def test_finalize_session(mock_db) -> None:
    # Arrange
    session_id = 1
    db.save_result(QuestionResult(id=None, quiz_sessions_id=session_id, question_text="Q1", user_answer="A", correct_answer="A", is_correct=True, response_time_ms=100.0))
    db.save_result(QuestionResult(id=None, quiz_sessions_id=session_id, question_text="Q2", user_answer="C", correct_answer="B", is_correct=False, response_time_ms=200.0))
    # Act
    avg_ms = db.finalize_session(session_id)
    # Assert
    assert avg_ms == 150.00