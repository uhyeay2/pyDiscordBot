from dataclasses import dataclass
from typing import List, Optional

@dataclass
class QuizQuestion:
    """Model representing a single question, regardless of source."""
    question_text: str
    correct_answer: str
    options: List[str]  # This will hold the shuffled A, B, C, D choices

@dataclass
class QuestionResult:
    """Model representing the result of a single question attempt."""
    id: Optional[int]
    quiz_sessions_id: int
    question_text: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    response_time_ms: float

@dataclass
class QuizSession:
    """Model representing an entire quiz session for a user."""
    id: Optional[int]
    user_id: int
    question_groups_id: Optional[int]
    average_response_ms: float
    started_at: str  # ISO format datetime string
    ended_at: Optional[str]  # ISO format datetime string