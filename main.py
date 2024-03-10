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
from sqlalchemy import create_engine, text
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


