import os
from dotenv import load_dotenv
from google import genai
import warnings
import json

warnings.filterwarnings("ignore")

import pandas as pd
from google.genai.types import GenerateContentConfig

load_dotenv()

# PROJECT_ID = str(os.environ.get("PROJECT_ID"))
# LOCATION = str(os.environ.get("LOCATION"))
MODEL_ID = "gemini-2.5-flash"  # @param {type: "string"}

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
        
        prompt = f"""Classify each YouTube comment as ACTIONABLE, SUPPORTIVE, or IRRELEVANT.
        - ACTIONABLE: specific feedback the creator can act on, whether positive or negative (e.g. "The audio is too quiet after the intro", "The explanation at 3:20 really helped me understand promises")
        - SUPPORTIVE: positive engagement but nothing specific to act on (e.g. "Great video!", "Thanks so much", "Love your content")
        - IRRELEVANT: doesn't relate to the content or provide any value — spam, memes, "first!", off-topic arguments, self-promotion

        Comments:
        {comments_text}
        Respond in JSON format only, no other text:
            [
                {{"index": 1, "category": "ACTIONABLE", "summary": "one sentence summary"}}
            ]
            """

        response = client.models.generate_content(
            model = MODEL_ID,
            contents = prompt,
            config = GenerateContentConfig(
                response_modalities=['TEXT']
            )
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