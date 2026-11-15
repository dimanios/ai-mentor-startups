# Здесь описана вспомогательная функция для запросов к llm на хосте
import os

from ollama import Client


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:4b")
client = Client(host=OLLAMA_HOST)


def ask_llm(history: list[dict]):
    response = client.chat(
        model=MODEL_NAME,
        messages=history,
        #think=False
    )
    return response