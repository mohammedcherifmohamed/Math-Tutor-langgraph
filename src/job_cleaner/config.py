from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

MODEL_NAME = "gemini-3.8-flash"

def get_model() : 
    return ChatGoogleGenerativeAI(model=MODEL_NAME)

model = get_model()

