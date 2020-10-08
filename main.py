from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer

import json
import os

CNF_FILE = "postgres.cnf.json"
UPLOAD_DIR = "upload_dir/"

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

@app.get('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}

@app.post("/index/")
def register(file: UploadFile = File(...)):
    file_name = UPLOAD_DIR + file.filename
    with open(file_name, 'wb') as f:
        f.write(file.file.read())
    print(file_name)

    file_extension = os.path.splitext(file_name)[1]
    print(file_extension, "file_ext")
    djv.fingerprint_directory(UPLOAD_DIR, [file_extension])
    # djv.fingerprint_file(str(file_name))
    os.remove(file_name)
    return True

@app.post("/find/")
def post(file: UploadFile = File(...)):
    file_name = UPLOAD_DIR + file.filename
    with open(file_name, 'wb') as f:
        f.write(file.file.read())
    results = djv.recognize(FileRecognizer, file_name)
    os.remove(file_name)
    return results


 