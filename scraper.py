from dotenv import load_dotenv
import requests
import os
import time
import pandas as pd
from googleapiclient.discovery import build
import isodate
from urllib.parse import urlparse, parse_qs

load_dotenv()

API_KEY = os.getenv('YT_API_KEY')
youtube = build("youtube", "v3", developerKey=API_KEY)

# Gets video id from youtube url
def parse_video_id(url):

    # parses url into different parts
    parsed_url = urlparse("https://www.youtube.com/watch?v=Ht-eLQH_uK0&t=3157s")
    
    # returns dictionary with keys v and t
    query_dict = parse_qs(parsed_url.query)
    return query_dict['v']
        

