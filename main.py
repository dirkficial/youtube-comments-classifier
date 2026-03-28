from scraper import get_video_comments, parse_video_id
from classifier import classify_comments, save_response

url = input("Enter YouTube video URL: ")
video_id = parse_video_id(url)

print(f"Fetching comments for video: {video_id}")
comments = get_video_comments(video_id)

print(f"Found {len(comments)} comments. Classifying...")
results = classify_comments(comments)

save_response(results)
print("Done! Results saved to output/results.csv")