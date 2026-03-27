# 📚 Quiz Application with Document-Based Question Generation and LLM Evaluation

**Name:** Chandrashekhar Umesh Mannur     
**USN:** 2BL22CS051      
**GitHub Username:** Chandrashekhar051   
**Department:** CSE     

---

## 🔹 Problem Statement

Build a quiz application that accepts a user-provided document as input, generates topic-based questions from the content, and evaluates user answers using a Large Language Model (LLM). The system should support document ingestion, question generation, answer scoring, feedback generation, and result summaries.

---

## 🔹 Objective

The objective of this project is to design and implement an end-to-end AI-powered quiz system that:
- Processes input documents
- Generates meaningful and context-aware questions
- Evaluates user responses intelligently
- Provides feedback and performance summaries

This project focuses on building a **complete, explainable, and modular system using only open-source tools and models**.

---

## 🔹 Tech Stack (Open Source Only)

- Python
- Streamlit (User Interface)
- PyMuPDF (PDF Processing)
- HuggingFace Transformers
- Ollama (Local LLM Runtime)
- Torch (CPU-based)

---

## 🔹 System Architecture


User Input (PDF)             
↓                                         
Text Extraction (PyMuPDF)               
↓                            
Text Chunking                         
↓                                    
Question Generation (Flan-T5)               
↓                                          
User Interaction (Streamlit UI)                
↓                                             
Answer Evaluation (Phi-2 via Ollama)               
↓                                               
Score + Feedback + Summary                   
                  

---

## 🔹 Project Structure


quiz-llm-app/                            
│                                     
├── app.py                               
├── requirements.txt                         
├── README.md                             
│                                    
├── utils/                                
│ ├── pdf_reader.py                        
│ ├── text_chunker.py                               
│                                            
├── modules/                               
│ ├── question_generator.py                        
│ ├── answer_evaluator.py                              
│                                              
├── data/                           
├── outputs/                                


---

## 🔹 Features

- Document upload and processing (PDF)
- Text extraction from documents
- Efficient text chunking for LLM processing
- Automatic question generation from content
- Interactive quiz interface
- LLM-based answer evaluation
- Score calculation and feedback generation
- Result summary display

---
