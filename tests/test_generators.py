from pydiscordbot.generators import generate_addition_quiz

def test_generate_addition_quiz_length():
    num_q = 10
    questions = generate_addition_quiz(num_q, 1, 10, 1, 10)
    assert len(questions) == num_q

def test_math_logic_accuracy():
    # Test that the question text matches the correct answer
    questions = generate_addition_quiz(1, 5, 5, 5, 5) # Forces 5 + 5
    q = questions[0]
    assert q.question_text == "What is 5 + 5?"
    assert q.correct_answer == "10"