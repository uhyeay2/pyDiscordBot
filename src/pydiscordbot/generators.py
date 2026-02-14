import random
from typing import List
from .models import QuizQuestion

def generate_addition_quiz(
    num_questions: int, 
    start_a: int, end_a: int, 
    start_b: int, end_b: int
) -> List[QuizQuestion]:
    """Generates a list of addition questions based on custom ranges."""
    questions: List[QuizQuestion] = []
    
    for _ in range(num_questions):
        a = random.randint(start_a, end_a)
        b = random.randint(start_b, end_b)
        correct_value = a + b
        
        # Generate options - we want to ensure they are somewhat close to the correct answer for 'difficulty'
        options = set()
        options.add(str(correct_value))  

        while len(options) < 4:
            # Random offset between -5 and 5, excluding 0
            offset = random.choice([i for i in range(-3, 3) if i != 0])
            wrong_val = correct_value + offset
            if wrong_val >= 0: # No negative answers for simple addition
                options.add(str(wrong_val))                        

        questions.append(QuizQuestion(
            question_text=f"What is {a} + {b}?",
            correct_answer=str(correct_value),
            options=list(options)
        ))
        
    return questions