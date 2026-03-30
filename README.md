# 📚 Quiz Application with Document-Based Question Generation and LLM Evaluation

**Name:** Chandrashekhar Umesh Mannur     
**USN:** 2BL22CS051      
**GitHub Username:** Chandrashekhar051   
**Department:** CSE     

---

## 🚀 Overview

This project is an AI-powered quiz system that transforms static documents into an interactive learning experience.

The system:

* Extracts content from documents (PDF, TXT, DOCX)
* Generates context-aware questions using an LLM
* Evaluates user answers using semantic similarity
* Provides detailed feedback and performance summary

The entire pipeline is built using **open-source models and libraries**, ensuring transparency and reproducibility.

---

## 🎯 Problem Understanding

The goal is not just to generate questions, but to build a **complete evaluation system** that:

* Understands document content
* Generates meaningful and diverse questions
* Evaluates subjective answers (not exact match)
* Provides interpretable scoring and feedback

This makes the problem significantly more complex than simple QA systems.

---

## 🔍 Research & Existing Systems

Before implementation, I studied existing solutions:

### Existing Approaches

* GPT-based quiz generators
* Retrieval-based QA systems
* EdTech evaluation platforms

### Observed Limitations

* Heavy reliance on closed APIs
* Lack of explainable scoring
* Poor handling of long documents
* Repetitive or low-quality questions

---

## 🧠 System Design (My Approach)

The system is designed as a modular pipeline:

### 1. Document Ingestion

* Supports PDF, TXT, DOCX
* Extracts clean raw text using PyMuPDF

### 2. Intelligent Chunking

* Splits document into semantic chunks
* Maintains context overlap between chunks
* Avoids LLM input length limitations

👉 **Why this matters:**
LLMs perform poorly on long unstructured text. Chunking improves both relevance and quality.

---

### 3. Question Generation (LLM)

* Model: T5 fine-tuned for question generation
* Strategy:

  * Extract key sentence as answer
  * Provide context + answer → generate question

👉 **Why this works:**
Instead of asking LLM to generate questions blindly, we guide it using:

* context
* expected answer

This improves quality and reduces hallucination.

---

### 4. Answer Evaluation (Core Innovation)

Instead of exact matching, I implemented:

#### Hybrid Scoring System

* **Semantic Similarity (65%)**

  * Uses SentenceTransformers
* **Keyword Overlap (35%)**

  * Captures important terms

👉 Final Score:
score = semantic + keyword weighted score

---

### 5. Feedback Generation

Based on evaluation:

* Excellent / Good / Partial / Needs Improvement
* Context-aware feedback messages

---

### 6. Session Management

* Tracks quiz progress
* Stores results
* Generates final summary
* Exports results as CSV

---

## 🔄 Iterations & Improvements

### ❌ Attempt 1: Direct Question Generation

* Input: full document
* Problem:

  * Repeated questions
  * Poor relevance

---

### ❌ Attempt 2: No Chunking

* Problem:

  * LLM confusion
  * Low-quality outputs

---

### ❌ Attempt 3: Only Semantic Scoring

* Problem:

  * Missed keyword importance
  * Over-scoring vague answers

---

### ✅ Final Approach

* Chunk-based processing
* Guided question generation (answer + context)
* Hybrid evaluation (semantic + keyword)

---

## ⚠️ Challenges Faced

### 1. Duplicate Questions

* Cause: Similar chunks
* Fix:

  * Random chunk sampling
  * Better chunking strategy

---

### 2. Long Document Handling

* Cause: LLM input limit
* Fix:

  * Chunking with overlap

---

### 3. Weak Answer Evaluation

* Cause: Simple string matching
* Fix:

  * Semantic similarity using embeddings

---

### 4. Model Hallucination

* Cause: Unguided prompts
* Fix:

  * Structured input: answer + context

---

### 5. Performance Issues (Colab)

* Cause: Model loading + CPU limits
* Fix:

  * Optimized chunk size
  * Reduced inference calls

---

## 📊 Final System Capabilities

* Multi-format document support
* Context-aware question generation
* Semantic answer evaluation
* Real-time feedback
* Performance summary & export

---

## 🛠️ Tech Stack (Open Source Only)

* Python
* PyMuPDF (PDF parsing)
* NLTK (text processing)
* SentenceTransformers (embeddings)
* HuggingFace Transformers (LLM)
* Gradio (UI)

---
## ▶️ How to Run

### Option 1: Google Colab
- Open notebook
- Run all cells step-by-step

### Option 2: Local Setup

- bash
- pip install -r requirements.txt
---

## 📚 Key Learnings

* LLMs require structured input, not raw text
* Chunking is critical for performance
* Evaluation is harder than generation
* Hybrid approaches outperform single methods
* Prompt design directly impacts output quality

---

## 🔮 Future Improvements

* Add MCQ generation
* Difficulty levels
* Better evaluation using LLM judge
* Deploy as web app
* Add leaderboard system

---

## 👨‍💻 Author

Chandrashekhar Mannur
