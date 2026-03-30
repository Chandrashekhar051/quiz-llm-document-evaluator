# 📚 Quiz Application with Document-Based Question Generation and LLM Evaluation

**Name:** Chandrashekhar Umesh Mannur     
**USN:** 2BL22CS051      
**GitHub Username:** Chandrashekhar051   
**Department:** CSE     

---

## 🚀 Overview

This project is an AI-powered quiz system that:
- Accepts a PDF document as input
- Generates questions from the content
- Evaluates user answers using an LLM
- Provides feedback and final score

The system is built using open-source tools and follows a modular pipeline.

---

## 🎯 Problem Statement

Build a quiz application that:
- Accepts a document as input
- Generates topic-based questions
- Evaluates answers using LLM
- Provides feedback and summary

---

## 🧠 Approach

### Step 1: Document Ingestion
- Extract text from PDF using PyMuPDF

### Step 2: Text Preprocessing
- Sentence tokenization using NLTK
- Cleaning and chunking

### Step 3: Embeddings
- Generate embeddings using SentenceTransformers

### Step 4: Question Generation
- Use FLAN-T5 model
- Prompt-based generation

### Step 5: Answer Evaluation
- Compare user answers with expected answers
- Use similarity scoring

### Step 6: Feedback
- Generate qualitative feedback

---

## 🛠️ Tech Stack

- Python
- Google Colab
- PyMuPDF (fitz)
- NLTK
- SentenceTransformers
- HuggingFace Transformers

---


