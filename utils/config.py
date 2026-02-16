import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def build_new_llm_client(temperature):
    return ChatOpenAI(
        model="gpt-4o",
        temperature=temperature,
        max_tokens=16000,
        api_key=os.getenv("OPENAI_API_KEY")
    )