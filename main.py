
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
from sqlalchemy import create_engine, text  # Keep both imports from master and JTN_Branch
import requests
import random
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import keyboard


def fetch_images_from_api(api_url):
    response = requests.get(api_url)
    data = response.json()
    memes_data = data.get('data', {}).get('memes', [])
    return memes_data


def select_random_image(images):
    return random.choice(images)


def display_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    plt.imshow(img)
    plt.axis('off')
    plt.show()


def analytics():
    with engine.connect() as connection:
        # top 10 captions analytics
        query_top_captions = text("SELECT name, captions FROM memes ORDER BY captions DESC LIMIT 10")
        result_top_captions = connection.execute(query_top_captions)
        top_captions = result_top_captions.fetchall()

        # lowest 10 captions analytics
        query_lowest_captions = text("SELECT name, captions FROM memes ORDER BY captions ASC LIMIT 10")
        result_lowest_captions = connection.execute(query_lowest_captions)
        lowest_captions = result_lowest_captions.fetchall()

        # average of all captions
        query_avg_caption = text("SELECT AVG(captions) FROM memes")
        result_avg_caption = connection.execute(query_avg_caption)
        avg_caption = result_avg_caption.scalar()

    return top_captions, lowest_captions, avg_caption


if __name__ == "__main__":

    # Fetch data from the API
    api_url = "https://api.imgflip.com/get_memes"
    memes_data = fetch_images_from_api(api_url)

    # Create DataFrame
    df = pd.DataFrame(memes_data)
    # Database connection
    db_host = '127.0.0.1'
    db_user = 'root'
    db_password = ''
    db_name = 'meme'

    # Create engine
    engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    # Create table
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
        connection.execute(text("DROP TABLE IF EXISTS memes"))
        connection.execute(text(create_table))

        # Insert the DataFrame into the database
        df.to_sql(name='memes', con=engine, if_exists='append', index=False)

    # Perform Analytics
    top_captions, lowest_captions, avg_caption = analytics()

    top_ten_memes = []
    top_ten_captions = []

    low_ten_memes = []
    low_ten_captions = []

    print("Top 10 captions with the highest values:")
    for captions, value in top_captions:
        top_ten_memes.append(captions)
        top_ten_captions.append(value)
    top = pd.DataFrame({
        "Name": top_ten_memes,
        "Captions": top_ten_captions
    })
    print(top)

    print("\nTop 10 captions with the lowest values:")
    for captions, value in lowest_captions:
        low_ten_memes.append(captions)
        low_ten_captions.append(value)
    low = pd.DataFrame({
        "Name": low_ten_memes,
        "Captions": low_ten_captions
    })
    print(low)


    print(f"\nAverage value of all captions: {avg_caption}")