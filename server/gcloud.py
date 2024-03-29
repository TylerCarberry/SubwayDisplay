import json
import os
from google.cloud import storage
from google.oauth2 import service_account

import utils

BUCKET_NAME = "subwaykindledisplay"


def authenticate_storage_client():
    if utils.is_running_on_pi():
        with open('/home/pi/keys/SUBWAY_DISPLAY_GOOGLE_KEY.json') as f:
            key = json.load(f)
    else:
        key = json.loads(os.environ["SUBWAY_DISPLAY_GOOGLE_KEY"])
    storage_credentials = service_account.Credentials.from_service_account_info(key)
    return storage.Client(credentials=storage_credentials)


def upload_blob(source_file_name, destination_blob_name):
    storage_client = authenticate_storage_client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    metadata = {'Cache-Control': 'no-cache, max-age=0'}
    blob.metadata = metadata

    blob.upload_from_filename(source_file_name)
    blob.make_public()
    blob.metadata = metadata

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
