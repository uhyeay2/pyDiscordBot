# pyDiscordBot

A Discord bot for running interactive quizzes. Currently supports math quizzes (addition), with extensible architecture for other question types.

## Features

- **Modular Quiz Engine**: Generic `run_quiz()` function handles any `QuizQuestion` type
- **Question Generators**: Math quiz generator with configurable ranges
- **Session Tracking**: Persistent SQLite database with user scores and response times
- **Discord Integration**: Async Discord.py bot with command handlers
- **Test Coverage**: Comprehensive unit tests with mocking and in-memory test DB

## Project Structure

```
src/pydiscordbot/
├── bot.py           # Discord bot commands (e.g., !addition)
├── quiz.py          # Core quiz engine (question flow, timing, scoring)
├── generators.py    # Question generation logic (e.g., addition problems)
├── database.py      # SQLite schema, session/result persistence
├── models.py        # Data models (QuizQuestion, QuestionResult, QuizSession)
└── __init__.py

tests/
├── test_bot.py      # Tests for command initialization
├── test_quiz.py     # Tests for quiz flow, timeouts, scoring
├── test_database.py # Tests for DB schema and operations
├── conftest.py      # PyTest fixtures (in-memory test DB)
└── __init__.py
```

## Installation

1. **Clone and navigate to project:**
   ```bash
   cd pyDiscordBot
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   source venv/bin/activate   # macOS/Linux
   ```

3. **Install package in development mode:**
   ```bash
   pip install -e .
   ```

4. **Set up Discord bot token:**
   Create a `.env` file in the root directory:
   ```
   DISCORD_BOT_TOKEN=your_token_here
   ```

## Running the Bot

```bash
venv\Scripts\Activate.ps1
python -c "from pydiscordbot.bot import run; run()"
```

### Bot Commands

- **`!addition [num_questions] [a_start] [a_end] [b_start] [b_end]`**
  - Starts an addition quiz with custom question count and value ranges
  - Defaults: 5 questions, operands range 1–20
  - Example: `!addition 10 1 100 1 100`

## Testing

Run all tests with coverage:
```bash
venv\Scripts\Activate.ps1
pytest --cov=src/pydiscordbot --cov-report=html --cov-report=xml tests/
```

Coverage reports:
- HTML: `htmlcov/index.html`
- XML: `coverage.xml`

Run specific test file:
```bash
pytest tests/test_quiz.py -v
pytest tests/test_bot.py -v
```

## Database

SQLite database (`pyDiscordBot.db`) with tables:
- `question_groups` — Question categories
- `questions` — Question templates
- `quiz_sessions` — User quiz attempts (score, duration)
- `questions_results` — Per-question results (timing, correctness)

Auto-initialized on bot startup.

## Architecture

### Quiz Flow

1. **Command** (`bot.py`): User types `!addition`
2. **Session creation** (`database.py`): New session ID generated
3. **Question generation** (`generators.py`): Questions created with shuffled options
4. **Quiz engine** (`quiz.py`): Options presented, user response timed, result saved
5. **Finalization** (`database.py`): Session closed, average response time recorded

### Models

- **`QuizQuestion`**: `question_text`, `correct_answer`, `options[]`
- **`QuestionResult`**: Session ID, answers, timing, correctness
- **`QuizSession`**: User ID, scores, session timestamps

## Development

Install dev dependencies (if added to `pyproject.toml`):
```bash
pip install pytest pytest-asyncio pytest-cov
```

Run tests in watch mode:
```bash
pytest tests/ -v --tb=short
```