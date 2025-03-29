import pandas as pd
from sqlalchemy import create_engine 


df = pd.read_csv('real_estate_clean.csv')

# Selecting columns to include (exclude the first three)
columns_to_include = df.columns[3:]
df_to_sql = df[columns_to_include]

engine = create_engine('sqlite:///real_estate.db')

# Writing the DataFrame to the SQL database
df_to_sql.to_sql('czech_RE', engine, if_exists='replace', index=False)

connection = engine.raw_connection()

read_df = pd.read_sql('SELECT * FROM czech_RE', connection) 

connection.close()

print(read_df)
