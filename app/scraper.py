from dotenv import load_dotenv
import os
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urlparse, parse_qs

load_dotenv()

API_KEY = os.getenv('YT_API_KEY')
youtube = build("youtube", "v3", developerKey=API_KEY)

# Gets video id from youtube url
def parse_video_id(url):
    parsed_url = urlparse(url)

    # Handle youtu.be short URLs
    if parsed_url.netloc == "youtu.be":
        return parsed_url.path.lstrip("/") or None

    query_dict = parse_qs(parsed_url.query)
    return query_dict.get('v', [None])[0]
        
def get_channel_id(video_id):
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    items = response.get('items', [])
    if not items:
        return None
    return items[0]['snippet']['channelId']

def get_all_replies(parent_id, channel_id):
    replies = []
    reply_page_token = None

    while True:
        request = youtube.comments().list(
            part = "snippet",
            parentId = parent_id,
            maxResults = 100,
            pageToken = reply_page_token,
            textFormat = "plainText"
        )

        response = request.execute()

        for reply in response['items']:
            details = reply['snippet']
            if details['authorChannelId']['value'] == channel_id:
                continue
            replies.append({
                "comment_text": details['textOriginal'],
                "like_count": details['likeCount'],
                "reply_count": 0
            })

        reply_page_token = response.get('nextPageToken')
        if not reply_page_token:
            break

    return replies

def get_video_comments(video_id):

    next_page_token = None
    comments = []
    channelID = get_channel_id(video_id)

    if channelID is None:
        return comments

    while True:
        try: 
            request = youtube.commentThreads().list(
                part = "snippet, replies",
                videoId = video_id,
                maxResults = 100,
                pageToken = next_page_token,
                textFormat = "plainText"
            )

            response = request.execute()

            for item in response['items']:
                comment_details = item['snippet']['topLevelComment']['snippet']
                if comment_details['authorChannelId']['value'] == channelID:
                    continue
                
                comments.append({
                    "comment_text" : comment_details['textOriginal'],
                    "like_count" : comment_details['likeCount'],
                    "reply_count" : item['snippet'].get('totalReplyCount', 0)
                    })
                
                if item['snippet'].get('totalReplyCount', 0) > 0:
                    comments.extend(get_all_replies(
                        item['snippet']['topLevelComment']['id'],
                        channelID
                    ))

            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

        except HttpError as e:
            if e.resp.status == 429:
                print("Rate limit hit, waiting 5 seconds...")
                time.sleep(5)
                continue
            else:
                print(f"Oops! There was an error trying to fetch comments for {video_id}: {e}")
                break
        except Exception as e:
            print(f"Oops! There was an error trying to fetch comments for {video_id}: {e}")
            break

    return comments