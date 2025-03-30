import google.generativeai as genai

genai.configure(api_key="AIzaSyAv-Nf9CJcQcpB8k0vM4P_rLNng49FkBxk")

models = genai.list_models()
for model in models:
    print(model.name, "-", model.supported_generation_methods)
