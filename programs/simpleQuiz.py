def ask_question(question, choices):
    print(question)
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    answer = int(input("Enter the number of your answer: ")) - 1
    return answer

def main():
    questions = [
        {
            "question": "What is the capital of France?",
            "choices": ["Berlin", "Madrid", "Paris", "Rome"],
            "correct": 2
        },
        {
            "question": "What is 2 + 2?",
            "choices": ["3", "4", "5", "6"],
            "correct": 1
        },
        {
            "question": "What is the color of the sky on a clear day?",
            "choices": ["Green", "Blue", "Red", "Yellow"],
            "correct": 1
        }
    ]

    score = 0

    for q in questions:
        user_answer = ask_question(q["question"], q["choices"])
        if user_answer == q["correct"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer was {q['choices'][q['correct']]}.")
        print("")

    print(f"Quiz complete! Your final score is: {score}/{len(questions)}")

if __name__ == "__main__":
    main()
