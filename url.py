import google.generativeai as genai
from googlesearch import search
import re
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

# Configure Gemini with the key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


UNWANTED_DOMAINS = ["amazon", "quora", "pinterest", "researchgate", "ieee", "sciencedirect", "wikipedia", "chegg"]

def get_top_search_results(query, num_results=20):
    
    try:
        results = list(search(query, num_results=num_results))
        time.sleep(1)  # Prevent API rate limit issues
        return results
    except Exception as e:
        print(f"Error fetching search results: {e}")
        return []

def filter_educational_urls(urls):
    
    
    filtered_urls = [url for url in urls if not any(domain in url for domain in UNWANTED_DOMAINS)]

    if not filtered_urls:
        return [] 

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Here is a list of article URLs:\n\n"
        + "\n".join(filtered_urls) +
        "\n\nSelect ONLY the top 3 **educational** links that provide useful study materials. "
        "Do NOT include product pages, forums, shopping websites, or paid content. "
        "Return ONLY the 3 URLs in plain text, one per line."
    )

    time.sleep(2)  
    response = model.generate_content(prompt)

    if not response.text.strip():
        print("Gemini returned an empty response! No URLs were filtered.")
        return []

    
    final_filtered_urls = re.findall(r"https?://[^\s]+", response.text)

    return final_filtered_urls[:3]  

def get_top_articles(query):
    
    links = get_top_search_results(query)

    if links:
        filtered_links = filter_educational_urls(links)
        return [{"title": f"Article {i+1}", "url": link} for i, link in enumerate(filtered_links)]
    else:
        return []

if __name__ == "__main__":
    topic = input("Enter search query: ")
    articles = get_top_articles(topic)

    if articles:
        print("\n✅ **Top 3 Educational Articles:**\n" + "-" * 50)
        for idx, article in enumerate(articles, start=1):
            print(f"{idx}. {article['title']} - {article['url']}")
    else:
        print("❌ No educational links found. Try a different query.")
