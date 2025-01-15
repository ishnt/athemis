from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
KEY=os.getenv("API_KEY")
def query_pdf_content(file_content, user_query):
    client = Groq(api_key=KEY)
    
    
    messages = [
        {
            "role": "system",
            "content": f"You are a PDF Chatbot designed to assist users with extracting and interacting with the content of PDF files. When a PDF is uploaded, extract its text and store it in memory. The content of the PDF is as follows:\n\n\n{file_content}"
        },
        {
            "role": "user",
            "content": user_query
        },
    ]
    
    
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=messages,
        temperature=0,
        max_tokens=7000,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    # Collect and print the responses
    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""
    
    return result
