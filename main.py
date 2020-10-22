from indexing_service import index_audio
from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache
import init
import globals
import requests

UPLOAD_DIR = "upload_dir/"

global_init()

def update_state(file):
    payload = {
        'topic_name': globals.RECEIVE_TOPIC,
        'client_id': globals.CLIENT_ID,
        'value': file
    }
    try:
        requests.request("POST", globals.DASHBOARD_URL,  data=payload)
    except: 
        print("EXCEPTION IN UPDATE STATE API CALL......")


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
        except:
            print("EXCEPTION IN GET PK... continue")
            continue

        # file_name = db_object.file_name
        # USING PK as file name to retrive it later in search api
        file_name = str(db_key)
        
        print("#############################################")
        print("########## PROCESSING FILE " + file_name)
        print("#############################################")

        file_path = UPLOAD_DIR + file_name

        with open(file_path, 'wb') as file_to_save:
            file_to_save.write(db_object.file.read())
        try:
            status = index_audio(file_path)
            print(f"AUDIO INDEXED {status}")
        except:
            print("ERROR IN INDEXING")
            continue
        
        print(".....................FINISHED PROCESSING FILE.....................")
        update_state(file_name)