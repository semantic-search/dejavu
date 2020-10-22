from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache
from indexing_service import index_audio
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer

import json
import os
import numpy as np

global_init()
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

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf8')
        return json.JSONEncoder.default(self, obj)

@app.get('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}

@app.post("/index/")
def register(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR + file.filename
    with open(file_path, 'wb') as f:
        f.write(file.file.read())

    index_audio(file_path) 

    return True

@app.post("/find/")
def post(file: UploadFile = File(...)):
    file_name = UPLOAD_DIR + file.filename
    with open(file_name, 'wb') as f:
        f.write(file.file.read())
    results = djv.recognize(FileRecognizer, file_name)
    os.remove(file_name)
    print(results)

    try:
        results_array = results["results"]
        first_song = results_array[0]

        song_pk = first_song["song_name"].decode()

        print("here 1", song_pk)
        try:
            db_object = Cache.objects.get(pk=song_pk)
            file_name = db_object.file_name
            results["data"] = {
                "file_name": file_name,
                "file_id": song_pk
            }
        except:
            print("EXCEPTION IN GET PK process")

    except AttributeError:
        print("No song in response")

    return json.dumps(results, cls=NumpyEncoder)


 