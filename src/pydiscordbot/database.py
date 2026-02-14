import sqlite3
from pydiscordbot.models import QuestionResult

DB_NAME = "pyDiscordBot.db"

def get_connection() -> sqlite3.Connection:
    """Returns a new connection to the SQLite database. The caller is responsible for closing it."""    
    # We use check_same_thread=False because Discord runs on an async loop 
    # and we want to allow multiple threads to access the DB connection without issues.
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS question_groups (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE NOT NULL)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            question_groups_id INTEGER,
                            question_text TEXT NOT NULL,
                            correct_answer TEXT NOT NULL,
                            wrong_1 TEXT, wrong_2 TEXT, wrong_3 TEXT,
                            FOREIGN KEY(question_groups_id) REFERENCES question_groups(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_sessions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            question_groups_id INTEGER,
                            average_response_ms REAL DEFAULT 0.0, 
                            started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            ended_at DATETIME,
                            FOREIGN KEY(question_groups_id) REFERENCES question_groups(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS questions_results (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            quiz_sessions_id INTEGER NOT NULL,
                            question_text TEXT NOT NULL,
                            user_answer TEXT NOT NULL,
                            correct_answer TEXT NOT NULL,
                            is_correct INTEGER,
                            response_time_ms REAL,
                            FOREIGN KEY(quiz_sessions_id) REFERENCES quiz_sessions(id))''')
        conn.commit()

def create_session(user_id: int, question_groups_id: int = None) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO quiz_sessions 
                       (user_id, question_groups_id) 
                       VALUES (?, ?)''', 
                       (user_id, question_groups_id))
        conn.commit()
        return cursor.lastrowid

def save_result(result: QuestionResult) -> None:
    with get_connection() as conn:
        conn.execute('''INSERT INTO questions_results 
                        (quiz_sessions_id, question_text, correct_answer, user_answer, is_correct, response_time_ms) 
                        VALUES (?, ?, ?, ?, ?, ?)''', 
                     (result.quiz_sessions_id, result.question_text, result.correct_answer, result.user_answer, 1 if result.is_correct else 0, round(result.response_time_ms, 2)))

def finalize_session(session_id: int) -> float:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(response_time_ms) FROM questions_results WHERE quiz_sessions_id = ?", (session_id,))
        avg_ms = cursor.fetchone()[0] or 0.0
        rounded_avg = round(avg_ms, 2)
        cursor.execute('''UPDATE quiz_sessions SET 
                            ended_at = CURRENT_TIMESTAMP, 
                            average_response_ms = ? 
                            WHERE id = ?''', 
                            (rounded_avg, session_id))
        conn.commit()
        return rounded_avg