import functions_framework
import pandas as pd
import logging
from flask import make_response
from utils.metrics_calculation import data_metric_count, upload_shape_to_gcs_trigger

logger = logging.getLogger('gcs_triggered_function_logger')
logger.setLevel(logging.INFO)

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def gcs_function_trigger(cloud_event):
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

            # Get shape of data frame in JSON format and store in bucket with same file name but .JSON
            try:
                data_shape_json = data_metric_count(df)
                # Upload JSON file to GCS
                upload_shape_to_gcs_trigger('gcs_trigger_function_report', name, data_shape_json)
                logger.info('Succesfully proceesed CSV data and uploaded JSON file with data summary')
                return make_response('File prioceesed succesfuly', 200)
            
            except Exception as e:
                return make_response((f"Error transofrming to JSON and uploading to GCS: {e}", 500))
                        
        except Exception as e:
            logger.error("Failed to read CSV %s: %s", uri, e, exc_info=True)
            return make_response((f"Error reading CSV: {e}", 500))
        
    else:
        return make_response('Did Not Recived CSV file handle exception', 204)