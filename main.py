from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer

import json
import os

CNF_FILE = "postgres.cnf.json"

with open(CNF_FILE, 'r') as f:
    config = json.load(f)

# create a Dejavu instance
djv = Dejavu(config)

 
app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/index/")
def register(file: UploadFile = File(...)):
    file_name = file.filename
    with open(file_name, 'wb') as f:
        f.write(file.file.read())
    print(file_name)
    djv.fingerprint_file(str(file_name))
    os.remove(file_name)
    return True

@app.post("/find/")
def post(file: UploadFile = File(...)):
    file_name = file.filename
    with open(file_name, 'wb') as f:
        f.write(file.file.read())
    results = djv.recognize(FileRecognizer, file_name)
    os.remove(file_name)
    return results


 