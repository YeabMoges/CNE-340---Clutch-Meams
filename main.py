
# Group Project Source Code
#
#
# Created database in LAMP/WAMP database
#
# code pulls data from a data source and puts data into Database
#             https://api.imgflip.com/get_memes
#
# code pulls data from database and analyzes analytics


import pandas as pd
from sqlalchemy import create_engine
import requests

# Fetch data from the API
api_url = "https://api.imgflip.com/get_memes"
response = requests.get(api_url)
data = response.json()

# Create DataFrame from API response data
df = pd.DataFrame(data)

# Database connection details
db_host = '127.0.0.1'
db_user = 'root'
db_password = ''
db_name = 'meme'

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# Define the table schema
create_table = """
CREATE TABLE IF NOT EXISTS memes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        url VARCHAR(255),
        width INT,
        height INT,
        box_count INT,
        captions INT
)
"""

# Execute the SQL command to create the table
with engine.connect() as connection:
    connection.execute(create_table )

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# Insert the DataFrame into the database
df.to_sql(name='gene', con=engine, if_exists='append', index=False)

# Dispose the engine
engine.dispose()
