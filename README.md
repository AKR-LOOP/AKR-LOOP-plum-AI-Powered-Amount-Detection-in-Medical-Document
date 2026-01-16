# AKR-LOOP-plum-AI-Powered-Amount-Detection-in-Medical-Document

# AI Document Extraction Backend API

This project is a FastAPI-based backend that extracts structured financial information from text or images of bills, receipts, and invoices using AI.

It supports:
- Text input processing
- Image input (AI-based OCR using Vision models)
- Amount extraction
- Currency detection
- Context classification (Total, Paid, Due)
- Structured JSON output with confidence scoring
- Guardrail handling for noisy documents

---

## Tech Stack

- Python 3.10+
- FastAPI
- OpenAI API (Vision + NLP)
- Uvicorn
- Ngrok (for public demo)
- Pydantic

---

## System Architecture

Client (Text / Image) >> FastAPI Backend >> AI Vision OCR (for Images) >> AI Text Normalization + Extraction >> Structured JSON Response


---

## Features

- Accepts raw text or scanned receipt images
- Extracts billing related fields automatically
- Handles OCR noise and formatting errors
- Returns machine-readable JSON output
- Supports guardrail fallback for invalid documents

---

## Project Structure



---

## Setup Instructions

### 1. Clone Repository

run following commands
git clone https://github.com/YOUR_USERNAME/ai-document-extractor.git
cd app
pip install -r requirements.txt
uvicorn app:app --reload


http://127.0.0.1:8000/docs

