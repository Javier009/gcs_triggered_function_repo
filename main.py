import functions_framework
import pandas as pd
import logging
from flask import make_response

logger = logging.getLogger('gcs_triggered_function_logger')
logger.setLevel(logging.INFO)

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    if '.csv' in name:
        print('Recived CSV file write more code here')
        uri = f"gs://{bucket}/{name}"
        try:
            logger.info("Reading CSV from %s", uri)
            df = pd.read_csv(uri)
            print(df.head())
            logger.info("Successfully read CSV from %s", uri)
                        
        except Exception as e:
            logger.error("Failed to read CSV %s: %s", uri, e, exc_info=True)
            return make_response((f"Error reading CSV: {e}", 500))
    else:
        return make_response('Did Not Recived CSV file handle exception', 204)