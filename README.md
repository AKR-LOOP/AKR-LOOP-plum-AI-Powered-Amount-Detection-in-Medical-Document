# AKR-LOOP-plum-AI-Powered-Amount-Detection-in-Medical-Document

This project is a Fast API-based backend that extracts structured financial information from text or images of bills, receipts, and invoices using AI.

It supports:
- Text input processing
- Image input (AI-based OCR using Vision models)
- Amount extraction
- Currency detection
- Context classification (Total, Paid, Due, Dis)
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


## Setup Instructions

Clone Repository and run below commands
```
run following commands
git clone https://github.com/YOUR_USERNAME/ai-document-extractor.git
cd app
pip install -r requirements.txt
uvicorn app:app --reload
http://127.0.0.1:8000/docs working link
```

Ngrok Setup Summary (Windows)
Download ngrok from:
```https://ngrok.com/download```

Extract ngrok.exe from the ZIP file.
Move ngrok.exe to C:\Windows\System32 (adds it to PATH).
Create a free account at https://ngrok.com and copy your Auth Token.
Run in Command Prompt:
```ngrok config add-authtoken YOUR_TOKEN```

Start your FastAPI server:
```uvicorn app:app --reload```
In a new terminal, start ngrok:run
```ngrok http 8000```
Copy the HTTPS URL shown : ``` https://chiropodial-matt-penetralian.ngrok-free.dev/docs ```

click on insert text
example: {"text": "Total: INR 1200 Paid: 1000 Due: 200 Discount: 10%"} / works same for image

output: {
  "result": {
    "currency": "INR",
    "amounts": [
      {
        "type": "Total",
        "value": 1200,
        "source": "Total: INR 1200"
      },
      {
        "type": "Paid",
        "value": 1000,
        "source": "Paid: 1000"
      },
      {
        "type": "Due",
        "value": 200,
        "source": "Due: 200"
      },
      {
        "type": "Discount",
        "value": 10,
        "source": "Discount: 10%"
      }
    ],
    "status": "ok"
  }
}



