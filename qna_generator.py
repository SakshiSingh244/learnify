import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

# Configure Gemini with the key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def generate_qna(topic):
    """Generates one question-answer pair with structured JSON output."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = {
        "parts": [
            {"text": (
                f"Create 1 question-answer pair about '{topic}'.\n"
                "Format requirements:\n"
                "1. Return ONLY valid JSON\n"
                "2. Structure: [{\"question\":\"...\",\"answer\":\"...\"}]\n"
                "3. Answer should be comprehensive (50-100 words)\n"
                "4. Include key concepts and examples where applicable"
            )}
        ]
    }

    try:
        response = model.generate_content(prompt)
        json_str = response.text.replace('```json', '').replace('```', '').strip()
        qna_list = json.loads(json_str)
        
        if not isinstance(qna_list, list) or len(qna_list) == 0:
            raise ValueError("Invalid response format")
            
        return qna_list[0]  # Return just the first (and only) Q&A
    
    except Exception as e:
        print(f"Generation error: {e}")
        return {
            "question": "Error in content generation",
            "answer": f"Please try again. Error: {str(e)}"
        }

def main():
    topic = input("Enter topic: ").strip()
    if not topic:
        print("Error: Topic cannot be empty")
        return
    
    print(f"\nGenerating 1 Q&A for '{topic}'...\n")
    qna = generate_qna(topic)
    
    print(f"❓ Question: {qna['question']}")
    print(f"📝 Answer: {qna['answer']}\n")
    print("-" * 80)

if __name__ == "__main__":
    main()
