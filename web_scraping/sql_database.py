import pandas as pd
from sqlalchemy import create_engine 


df = pd.read_csv('real_estate_clean.csv')

# Select columns to include (exclude the first three)
columns_to_include = df.columns[3:]
df_to_sql = df[columns_to_include]

# Create an SQLite engine (you can change this for other databases)
engine = create_engine('sqlite:///real_estate.db')  # Creates a file named 'my_database.db'

# Write the DataFrame to the SQL database
df_to_sql.to_sql('czech_RE', engine, if_exists='replace', index=False)

# Optional: You can read data from the database to check
# Get the raw connection from the engine
connection = engine.raw_connection()

read_df = pd.read_sql('SELECT * FROM czech_RE', connection)  # Pass the raw connection

# Close the raw connection when you're done
connection.close()

print(read_df)