import pandas as pd
import json
from  google.cloud import storage

def data_metric_count(df):

    '''Args a python data frame
        Returns: a JSON object with the shape of the data frame
    '''

    df_shape = df.shape
    df_shape_dict = {'Rows': df_shape[0],
                     'Columns': df_shape[1]}

    df_shape_dict_json = json.dumps(df_shape_dict)

    return df_shape_dict_json
    

def upload_shape_to_gcs_trigger(bucket_name, file_name, json_object):
    """Cloud Storage trigger function to upload DataFrame shape as JSON."""
    try:
        #  uri = 'gs://{bucket_name}/{file_name}.json'
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob_name = f'{file_name}_shape.json'
        blob = bucket.blob(blob_name)
        blob.upload_from_string(json_object, content_type='application/json')
        print(f"Shape uploaded to: gs://{bucket_name}/f'{blob_name}")

    except Exception as e:
        print(f"Error processing file: {e}")
    

    