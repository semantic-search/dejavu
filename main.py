from indexing_service import index_audio
from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache
import init
import globals
import os
import requests 
from init import ERR_LOGGER

UPLOAD_DIR = "upload_dir/"

global_init()

FILE_ID = ""

def update_state(file_name):
    payload = {
        'parent_name': globals.PARENT_NAME,
        'group_name': globals.GROUP_NAME,
        'container_name': globals.RECEIVE_TOPIC,
        'file_name': file_name,
        'client_id': globals.CLIENT_ID
    }
    try:
        requests.request("POST", globals.DASHBOARD_URL,  data=payload)
    except Exception as e:
        print(f"{e} EXCEPTION IN UPDATE STATE API CALL......")
        ERR_LOGGER(f"{e} EXCEPTION IN UPDATE STATE API CALL......FILE ID {FILE_ID}")


if __name__ == "__main__":
    print('main fxn')
    print("Connected to Kafka at " + globals.KAFKA_HOSTNAME + ":" + globals.KAFKA_PORT)
    print("Kafka Consumer topic for this Container is " + globals.RECEIVE_TOPIC)
    for message in init.consumer_obj:
        message = message.value
        db_key = str(message)
        print(db_key, 'db_key')
        try:
            db_object = Cache.objects.get(pk=db_key)
        except Exception as e:
            print("EXCEPTION IN GET PK... continue")
            ERR_LOGGER(f"{e} EXCEPTION IN GET PK... continue")
            continue

        db_file_name = db_object.file_name
        file_extension = os.path.splitext(db_file_name)[1]
        # USING PK as file name to retrive it later in search api
        file_name = str(db_key) + file_extension
        
        print("#############################################")
        print("########## PROCESSING FILE " + file_name)
        print("#############################################")

        file_path = UPLOAD_DIR + file_name

        with open(file_path, 'wb') as file_to_save:
            file_to_save.write(db_object.file.read())
        try:
            status = index_audio(file_path)
            print(f"AUDIO INDEXED {status}")
        except Exception as e:
            print(f"{e} ERROR IN INDEXING")
            ERR_LOGGER(f"{e} ERROR IN INDEXING")
            continue
        
        print(".....................FINISHED PROCESSING FILE.....................")
        update_state(file_name)
