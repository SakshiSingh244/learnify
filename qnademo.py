import google.generativeai as genai


genai.configure(api_key="AIzaSyAv-Nf9CJcQcpB8k0vM4P_rLNng49FkBxk")

def generate_qna(topic, num_questions=5):
    model = genai.GenerativeModel("gemini-1.5-pro")  # Choose the right model
    prompt = f"Generate {num_questions} question-answer pairs on the topic '{topic}'. Provide a mix of MCQs and short-answer questions."

    response = model.generate_content(prompt)

    return response.text if response else "Failed to generate QnA"

if __name__ == "__main__":
    topic = input()
    qna = generate_qna(topic)
    print(qna)
