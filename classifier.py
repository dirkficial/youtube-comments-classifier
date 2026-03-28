import os
from dotenv import load_dotenv
from google import genai
import vertexai
import warnings
import json

warnings.filterwarnings("ignore")

import pandas as pd
from vertexai.generative_models import GenerationConfig, GenerativeModel

load_dotenv()
PROJECT_ID = str(os.getenv("GOOGLE_CLOUD_PROJECT"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("LOCATION_ID"))

generation_model = GenerativeModel("gemini-2.5-flash")
generation_config = GenerationConfig(temperature=0.1, max_output_tokens=256)


def classify_comments(comments):
    results = []
    
    like_counts = [c['like_count'] for c in comments]
    max_likes = max(like_counts) if like_counts else 1
    high_threshold = max_likes * 0.3
    medium_threshold = max_likes * 0.1

    for i in range(0, len(comments), 10):
        batch = comments[i:i+10]
        
        comments_text = ""
        for j, comment in enumerate(batch):
            comments_text += f'{j+1}. "{comment["comment_text"]}" (Likes: {comment["like_count"]})\n'
        
        prompt = f"""Classify each YouTube comment as POSITIVE, NEGATIVE, or GARBAGE.
        - POSITIVE: constructive feedback praising something specific
        - NEGATIVE: constructive feedback criticizing something specific  
        - GARBAGE: spam, memes, "first!", emoji-only, off-topic, generic praise with no detail

        Respond in JSON format only, no other text:
            [
                {{"index": 1, "category": "POSITIVE", "summary": "one sentence summary"}}
            ]

        Comments:
        {comments_text}"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            generation_config = generation_config,
            contents=prompt
        )
        
        try:
            text = response.text.strip()
            text = text.replace("```json", "").replace("```", "").strip()
            classifications = json.loads(text)
            
            for k, classification in enumerate(classifications):
                comment = batch[k]
                comment["category"] = classification["category"]
                comment["summary"] = classification["summary"]
                
                likes = comment["like_count"]
                if likes >= high_threshold:
                    comment["importance"] = "HIGH"
                elif likes >= medium_threshold:
                    comment["importance"] = "MEDIUM"
                else:
                    comment["importance"] = "LOW"
                    
                results.append(comment)
        except Exception as e:
            print(f"Error parsing batch {i}: {e}")
            for comment in batch:
                comment["category"] = "ERROR"
                comment["summary"] = "Classification failed"
                comment["importance"] = "N/A"
                results.append(comment)
    
    return results

def save_response(response):
    response_df = pd.DataFrame(response)
    os.makedirs("output", exist_ok=True)
    response_df.to_csv("./output/results.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(response)} to results.csv")