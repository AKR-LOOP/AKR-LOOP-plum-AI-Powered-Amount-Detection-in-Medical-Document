
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import base64

# -------------------------------
# LOAD ENV
# -------------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found")

# -------------------------------
# OPENAI CLIENT
# -------------------------------

client = OpenAI(api_key=api_key)

MODEL_NAME = "gpt-4.1-mini"

# -------------------------------
# FASTAPI APP
# -------------------------------

app = FastAPI(title="AI Text Normalization & Extraction API")

# -------------------------------
# INPUT MODEL
# -------------------------------

class TextInput(BaseModel):
    text: str

# -------------------------------
# OPENAI PROMPT
# -------------------------------

SYSTEM_PROMPT = """
You are a smart document extraction AI.

Your tasks:

1. Normalize the input text (fix OCR mistakes, spacing, spelling).
2. Extract important key-value pairs related to billing or finance
   (example: TOTAL, TAX, PAID, BALANCE, AMOUNT).
3. Extract all numbers found and currency.
4. Produce structured JSON output.
5. Calculate a confidence score (0 to 10) based on extraction quality.
6. if its does'nt look like a billing thing 
output should be like this 
{"status":"no_amounts_found","reason":"document too noisy"}

Output ONLY valid JSON.
Output ONLY valid JSON in this format:
Expected Output (JSON):
{
 "raw_tokens": [all extracted numbers in list format],
 "currency": "identify the symbol/ example usd, inr",
 "confidence":
}

{
  "normalized_amount": [fix mistake in all extracted numbers],
  "extracted_fields": [identify all possible key value pairs
     {"key": "", "value": ""}
  ],

}

final output in tis format
{
 "currency": "",
 "amounts": [
  {"type":"","value":,"source":"text: 'Total: currency number'"},
 ],
 "status":"ok"
}
"""

# -------------------------------
# IMAGE → TEXT USING AI (VISION OCR)
# -------------------------------

def extract_text_from_image_ai(image_bytes):

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "Extract ALL readable text from this image. Return ONLY plain text."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract text from this bill or receipt"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content

# -------------------------------
# OPENAI PROCESS FUNCTION
# -------------------------------

def process_with_openai(text: str):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.1
    )

    ai_output = response.choices[0].message.content

    try:
        return json.loads(ai_output)
    except:
        return {
            "error": "AI returned invalid JSON",
            "raw_output": ai_output
        }

# -------------------------------
# ENDPOINT 1 — INSERT TEXT
# -------------------------------

@app.post("/insert-text")
def insert_text(data: TextInput):

    result = process_with_openai(data.text)

    return {
        "result": result
    }

# -------------------------------
# ENDPOINT 2 — UPLOAD FILE (TEXT + IMAGE)
# -------------------------------

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):

    contents = await file.read()

    if file.content_type.startswith("image"):
        extracted_text = extract_text_from_image_ai(contents)

    else:
        try:
            extracted_text = contents.decode("utf-8")
        except:
            return {"error": "Unsupported file type"}

    result = process_with_openai(extracted_text)

    return {
        "filename": file.filename,
        "result": result
    }
