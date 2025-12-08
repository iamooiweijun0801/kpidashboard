from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import shutil
import os

app = FastAPI()

# Allow your frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

EXCEL_FILE = "test KPI.xlsx"
UPLOAD_PASSWORD = "Cellcard@2025"  # Set your own secret

# Root route to check if backend is live
@app.get("/")
def root():
    return {"message": "KPI backend is running!"}

def read_excel_to_json():
    if not os.path.exists(EXCEL_FILE):
        return []
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    df = df.fillna(0)
    return df.to_dict(orient='records')

@app.get("/api/kpis")
def get_kpis():
    """
    Returns KPI data as JSON
    """
    return {"kpis": read_excel_to_json()}

@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...), password: str = Form(...)):
    """
    Upload a new Excel securely
    """
    if password != UPLOAD_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    with open(EXCEL_FILE, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "success", "filename": file.filename}
