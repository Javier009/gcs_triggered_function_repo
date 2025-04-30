import pandas as pd
import random
import string


n_columns =  random.randint(1, 10)
n_rows =  random.randint(1, 1000)

col_names_avilable = ['ColA', 'ColB', 'ColC', 'ColD', 'ColE', 'ColF', 'ColG', 'ColH', 'ColI', 'ColJ']
df_col_names = col_names_avilable[0:n_columns]

data_dict  = {}

for column in  df_col_names:
    data_type = random.randint(0, 1) # 0 for string 1 for int 
    if data_type == 0:
        data = [random.choice(string.ascii_letters) for i in range(0,n_rows)]       
    else:
        data = [random.randint(1, 1000) for i in range(0,n_rows)]
    data_dict[column] = data

# Genearate mock data data frame 
df_mock = pd.DataFrame(data_dict)
print(df_mock.head())




