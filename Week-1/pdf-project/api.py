import numpy as np
import pandas as pd
import shutil
from PIL import Image
import pytesseract
import re
from fastapi import FastAPI, Path, Query, HTTPException, status, UploadFile, File

app = FastAPI()


@app.get("/")
def home():
    return {"Welcome!": "Thank you for using my API"}

@app.post("/upload/{id}")
async def upload_file(id: int = Path(..., description = 'Unique ID...'),  file: UploadFile = File(..., description = 'Add Files...')):
    credentials_df = pd.read_csv("credentials.csv")
    if id not in credentials_df["id"].to_list():
        with open(f'{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        credentials_df.loc[len(credentials_df)] = [id, file.filename]
        credentials_df.to_csv('credentials.csv', index=False)
        return{"Upload Succesful!": "{file.filename} was succesfully added."}
    else:
        return{f"Can't add {file.filename} because a file with that ID already exists": "Specify a different ID."}

@app.get("/get-taken-id")
def get_taken_id():
    credentials_df = pd.read_csv("credentials.csv")
    return credentials_df["id"].to_list()


@app.get("/get-total-by-id/{id}")
def get_total_by_id(id: int = Path(..., description = 'Unique ID...')):
    credentials_df = pd.read_csv("credentials.csv")
    if id in credentials_df["id"].to_list():
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        text = str(((pytesseract.image_to_string(Image.open(f"{credentials_df[credentials_df['id'] == id]['filename'].values[0]}")))))
        text = text.replace(',', '')
        lst = re.findall('[-+]?([0-9]+\.[0-9]*)[^%]', text)
        lst = np.array([float(i) for i in lst])
        return(lst.max())
    if id not in credentials_df["id"].to_list():
        raise HTTPException(status_code = 404, detail = "ID does no exist.")