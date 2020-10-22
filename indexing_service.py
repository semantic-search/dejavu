from dejavu import Dejavu
import json
import os

CNF_FILE = "postgres.cnf.json"
UPLOAD_DIR = "upload_dir/"

with open(CNF_FILE, 'r') as f:
    config = json.load(f)

# create a Dejavu instance
djv = Dejavu(config)

def index_audio(file_path):
    file_extension = os.path.splitext(file_path)[1]
    print(file_extension, "file_ext")
    djv.fingerprint_directory(UPLOAD_DIR, [file_extension])
    os.remove(file_path)
    return True