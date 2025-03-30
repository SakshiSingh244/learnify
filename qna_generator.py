import google.generativeai as genai
import json
import time

genai.configure(api_key="AIzaSyAv-Nf9CJcQcpB8k0vM4P_rLNng49FkBxk")

def generate_qna(topic, num_questions=5):
    """Generates Q&A pairs with structured JSON output."""
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    
    prompt = {
        "parts": [
            {"text": (
                f"Create {num_questions} question-answer pairs about '{topic}'.\n"
                "Format requirements:\n"
                "1. Return ONLY valid JSON\n"
                "2. Structure: [{\"question\":\"...\",\"answer\":\"...\"},...]\n"
                "3. Answers should be comprehensive (50-100 words)\n"
                "4. Include key concepts and examples where applicable"
            )}
        ]
    }

    try:
        response = model.generate_content(prompt)
        # Improved JSON extraction
        json_str = response.text.replace('```json', '').replace('```', '').strip()
        qna_list = json.loads(json_str)
        
        # Validate structure
        if not isinstance(qna_list, list):
            raise ValueError("Invalid response format")
            
        return qna_list[:num_questions]  # Ensure correct number
    
    except Exception as e:
        print(f"Generation error: {e}")
        return [{
            "question": "Error in content generation",
            "answer": f"Please try again. Error: {str(e)}"
        }]

def main():
    topic = input("Enter topic: ").strip()
    if not topic:
        print("Error: Topic cannot be empty")
        return
    
    print(f"\nGenerating Q&A for '{topic}'...\n")
    qna_pairs = generate_qna(topic)
    
    for i, pair in enumerate(qna_pairs, 1):
        print(f"❓ Question {i}: {pair['question']}")
        print(f"📝 Answer: {pair['answer']}\n")
        print("-" * 80)

if __name__ == "__main__":
    main()