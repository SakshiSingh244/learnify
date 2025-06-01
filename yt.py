from googleapiclient.discovery import build
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()  

# Configure Gemini with the key from .env
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_top_youtube_video(topic):

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    
    search_response = youtube.search().list(
        q=topic,
        part="id,snippet",
        type="video",
        maxResults=5,  
    ).execute()


    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

    if not video_ids:
        return {"title": "No video found", "url": ""}

    
    video_details = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids),
    ).execute()

    sorted_videos = sorted(
        video_details.get("items", []),
        key=lambda vid: int(vid["statistics"].get("likeCount", 0)),
        reverse=True,
    )

    top_video = sorted_videos[0]
    video_title = top_video["snippet"]["title"]
    video_url = f"https://www.youtube.com/watch?v={top_video['id']}"

    return {"title": video_title, "url": video_url}

if __name__ == "__main__":
    topic = input("Enter topic: ")
    top_video = get_top_youtube_video(topic)
    print(f"Title: {top_video['title']}\nURL: {top_video['url']}")
