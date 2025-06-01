import google.generativeai as genai
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

# Configure Gemini with the key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_chapters_and_topics(subject):
    """Get structured curriculum with validation."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = {
        "parts": [
            {"text": (
                f"Create a comprehensive course outline for '{subject}' with:\n"
                "- 5-8 main chapters\n"
                "- 3-5 topics per chapter\n"
                "Return ONLY valid JSON in this exact format:\n"
                "{\"Chapter 1\": [\"Topic 1.1\", \"Topic 1.2\"], ...}\n"
                "Important:\n"
                "1. Topics should cover fundamental to advanced concepts\n"
                "2. Include practical applications where relevant\n"
                "3. Maintain academic rigor"
            )}
        ]
    }

    try:
        time.sleep(1.5)  
        response = model.generate_content(prompt)
        
        
        json_str = response.text.split("```json")[-1].split("```")[0].strip()
        data = json.loads(json_str)
        
        
        if not isinstance(data, dict) or not all(isinstance(v, list) for v in data.values()):
            raise ValueError("Invalid structure")
            
        return data
    
    except Exception as e:
        print(f"API Error: {e}")
        return {"Error": ["Failed to generate content"]}

def display_outline(outline):
    
    print(f"\n📚 Course Outline Structure:")
    for chapter, topics in outline.items():
        print(f"\n📖 {chapter}:")
        for topic in topics:
            print(f"  • {topic}")

if __name__ == "__main__":
    subject = input("Enter subject name: ").strip()
    if not subject:
        print("Error: Subject name required")
    else:
        outline = get_chapters_and_topics(subject)
        display_outline(outline)