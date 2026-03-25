from dotenv import load_dotenv
import requests
import os
import time
import pandas as pd
from googleapiclient.discovery import build
import isodate
from urllib.parse import urlparse, parse_qs
import json

load_dotenv()

API_KEY = os.getenv('YT_API_KEY')
youtube = build("youtube", "v3", developerKey=API_KEY)

# Gets video id from youtube url
def parse_video_id(url):

    # parses url into different parts
    parsed_url = urlparse(url)
    
    # returns dictionary with keys v and t
    query_dict = parse_qs(parsed_url.query)
    return query_dict['v'][0]
        

def get_video_comments(video_id):

    next_page_token = None
    comments = []
    
    while True:
        try: 
            request = youtube.commentThreads().list(
                part = "snippet, replies",
                videoId = video_id,
                maxResults = 5,
                pageToken = next_page_token,
                textFormat = "plainText"
            )

            response = request.execute()

            for item in response['items']:
                comment_details = item['snippet']['topLevelComment']['snippet']
                # if comment_details['authorDisplayName'] is equal to channel owner:
                    # break
                
                comments.append({
                    "comment_text" : comment_details['textOriginal'],
                    "like_count" : comment_details['likeCount'],
                    "reply_count" : item['snippet'].get('totalReplyCount', 0)
                    })
                if item.get('replies'):
                    for reply in item['replies']['comments']:
                        reply_details = reply['snippet']
                        # if reply_details['authorDisplayName'] is equal to channel owner:
                            # break
                        comments.append({
                            "reply_text" : reply_details['textOriginal'],
                            "like_count" : reply_details['likeCount']
                            })

            # next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

            time.sleep(1)
        except Exception as e:
            print(f"Oops! There was an error trying to fetch comments for {video_id}: {e}")
            break

    return comments

def save_comments():
    return


def load_existing_comments():
    return

