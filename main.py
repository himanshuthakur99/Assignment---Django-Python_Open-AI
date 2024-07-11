# Python Fast API Developer with Open AI/LLMs - Himanshu Dangi
# File: main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import openai
import fitz  # PyMuPDF
import os

app = FastAPI()

# Ensure directories exist
if not os.path.exists("files"):
    os.makedirs("files")
if not os.path.exists("sessions"):
    os.makedirs("sessions")


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_location = f"files/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Extract text from PDF
        doc = fitz.open(file_location)
        text = ""
        for page in doc:
            text += page.get_text()  # type: ignore

        # Store the text in a session file
        session_id = file.filename  # Simplified for this example
        with open(f"sessions/{session_id}.txt", "w") as session_file:
            session_file.write(text)

        return JSONResponse(
            content={
                "message": "PDF uploaded and text extracted successfully.",
                "session_id": session_id,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query_pdf/")
async def query_pdf(query: str, session_id: str):
    try:
        # Load the text from the session file
        with open(f"sessions/{session_id}.txt", "r") as session_file:
            text = session_file.read()

        # Use OpenAI to process the query
        response = openai.ChatCompletion.create(  # type: ignore
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Here is the document text: {text}. Now answer the following question: {query}",
                },
            ],
        )

        answer = response["choices"][0]["message"]["content"]
        return JSONResponse(content={"response": answer})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Start the server with: uvicorn main:app --reload
