import os
import requests
import json
API_KEY = os.environ.get("API_KEY")

def generate_ai_questions(num_questions, subject, standard, content_type, topic):

    # FALLBACK (LOAD FROM JSON FILE)
    def fallback():
        print("AI failed, fallback to sample questions")

        try:
            with open("sample_questions.json", "r") as f:
                data = json.load(f)

            num_questions = 10
            # Ensure enough questions
            questions = data[:num_questions]

            formatted = []
            for q in questions:
                if (
                    "question" in q and
                    "options" in q and
                    "correct_option" in q and
                    len(q["options"]) == 4
                ):
                    formatted.append({
                        "question": q["question"],
                        "options": q["options"],
                        "correct_option": q["correct_option"]
                    })

            # If insufficient valid questions → still safe fallback
            if len(formatted) != num_questions:
                raise Exception("Invalid sample JSON")

            return formatted

        except Exception:
            # Last-resort fallback (should rarely happen)
            return [
                {
                    "question": "Fallback question",
                    "options": ["A", "B", "C", "D"],
                    "correct_option": 0
                }
                for _ in range(num_questions)
            ]

    # Difficulty logic
    difficulty = "Easy"
    try:
        std = int(standard)
        if std >= 9:
            difficulty = "Medium"
        if std >= 11:
            difficulty = "Hard"
    except:
        pass

    # PROMPT (YOUR SPEC)
    prompt = f"""
Return ONLY valid JSON. No explanation.

Format:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correct_option": integer
    }}
  ]
}}

Instructions:

Generate exactly {num_questions} multiple choice questions.

Subject: {subject}
Class: {standard}
Difficulty: {difficulty}

Content Type:
{content_type}

Rules:
- Questions must be appropriate for the given class level
- Use clear, simple, and age-appropriate language
- Each question must be unique and non-repetitive
- Only ONE correct answer per question
- Do NOT include "All of the above" or "None of the above"
- Options must be distinct, meaningful, and plausible
- Keep each question concise (maximum ~20 words)
- Each option should be short (preferably 1–6 words)

Content Instructions:
- If content_type = "Topic Description":
  Base the questions on the topic provided below
- If content_type = "Lesson Content":
  Generate questions strictly within the provided content
  Do NOT include knowledge outside the given content

INPUT:
{topic}

STRICT REQUIREMENTS:
- Output must be valid JSON
- No trailing commas
- No comments or explanations
- correct_option must be an integer from 0 to 3
"""

    try:
        VERIFY_SSL = os.environ.get("VERIFY_SSL", "true").lower() == "true"

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            verify=VERIFY_SSL,   # controlled
            data=json.dumps({
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }),
            timeout=30
        )

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # Parse JSON safely
        try:
            parsed = json.loads(content)
        except:
            return fallback()

        if "questions" not in parsed:
            return fallback()

        final_questions = []

        for q in parsed["questions"]:
            if (
                "question" not in q or
                "options" not in q or
                "correct_option" not in q
            ):
                return fallback()

            if len(q["options"]) != 4:
                return fallback()

            correct_option = q["correct_option"]

            if not isinstance(correct_option, int) or correct_option not in [0, 1, 2, 3]:
                return fallback()

            final_questions.append({
                "question": q["question"],
                "options": q["options"],
                "correct_option": correct_option
            })

        if len(final_questions) != num_questions:
            return fallback()

        return final_questions

    except Exception:
        return fallback()