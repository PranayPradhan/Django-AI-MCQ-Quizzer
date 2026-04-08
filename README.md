z# AI Quizzer

An AI-powered end-to-end MCQ quiz platform built with Django and OpenRouter, enabling teachers to create, assign, and evaluate quizzes efficiently.

---

##  Description

Allows teachers to generate multiple-choice questions using AI, assign quizzes to students, and track their performance. 
It provides a complete workflow from quiz creation to result evaluation, with a fallback mechanism to ensure reliability even if AI fails.

---

## Workflow

1. **Create Quiz**
   Teacher enters topic or lesson content → AI generates MCQs

2. **Review & Publish**
   Teacher reviews and edits questions → publishes quiz

3. **Assign Quiz**
   Teacher assigns quiz to a class/section with a date

4. **Student Attempt**
   Students attempt quiz on assigned date

5. **Evaluation & Report**
   Scores are calculated automatically → teacher can view reports

---

## AI Integration (OpenRouter)

* Uses OpenRouter API for AI-based question generation
* Model used: **openai/gpt-oss-20b**
* Ensures:

  * Structured JSON output
  * Valid MCQs (4 options, 1 correct answer)
  * Fallback to placeholder questions and option, if AI fails

---

## Tech Stack

* Backend: Django
* Frontend: HTML + Bootstrap
* Database: SQLite
* AI: OpenRouter API

---

## Reliability

* AI failure handling with placeholder questions and options which the teacher is required to fill at review time.
* Input validation for all generated questions
* Safe deployment using environment variables

---

## Notes

* This is currently an MVP
* Focus is on simplicity, reliability, and end-to-end workflow
