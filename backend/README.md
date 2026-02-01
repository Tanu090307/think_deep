# Backend API Design

## Health Check
GET /health
Response:
{"status": "ok"}

## Upload Book
POST /upload-book
Input: PDF file
Output: book_id

## Select Book
POST /select-book
Input: book_id
Output:confirmation

## Generate Summary
POST /generate-summary
Input: topic, book_id
Output: topic-wize summary

## Generate Flashcards
POST /generate-flashcards
Input: topic, book_id
Output: list of flashcards

## Generate Quiz
POST /generate-guiz
Input: topic, book_id
Output: quiz questions + answers