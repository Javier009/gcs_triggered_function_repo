import pandas as pd
import random
import string
import gcsfs
import uuid


def generate_random_df():
    n_columns =  random.randint(1, 10)
    n_rows =  random.randint(1, 1000)

    col_names_avilable = ['ColA', 'ColB', 'ColC', 'ColD', 'ColE', 'ColF', 'ColG', 'ColH', 'ColI', 'ColJ']
    df_col_names = col_names_avilable[0:n_columns]

    data_dict  = {}

    for column in  df_col_names:
        data_type = random.randint(0, 1)  # 0 for string 1 for int 
        if data_type == 0:
            data = [random.choice(string.ascii_letters) for i in range(0,n_rows)]       
        else:
            data = [random.randint(1, 1000) for i in range(0,n_rows)]
        data_dict[column] = data

    # Genearate mock data data frame 
    df_mock = pd.DataFrame(data_dict)
    return df_mock


def send_data_gcs(bucket_name='raw_data_gcs_trigger_function', file_name=f'random_file_{uuid.uuid4().hex}'):
    data = generate_random_df()
    gcs_uri = f'gs://{bucket_name}/{file_name}.csv'

    try:
        data.to_csv(gcs_uri, index=False) 
        print(f"DataFrame successfully uploaded to: {gcs_uri}")
        return True
    except Exception as e:
        print(f"Error uploading DataFrame to GCS: {e}")
        return False
    

if __name__ == '__main__':
    send_data_gcs()

    
    



