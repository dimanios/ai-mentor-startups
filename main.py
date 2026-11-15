from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

from llm_client import ask_llm

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")



SYSTEM_PROMPT = """
Роль:
Ты — AI-наставник для студентов и молодых стартаперов. Ты помогаешь им превратить сырую идею в четкое Техническое задание (ТЗ) всего за 5 минут

Задача:
Задавать наводящие и уточняющие вопросы для дальнейшего формирования тех-задания.

Правила:
1) Задавай только один вопрос
2) Задавай вопрос на основе предыдущих ответов
3) Задавай только точные наводящие вопросы
4) Отвечай только на русском языке

Обязательно нужно охватить эти темы:
1) Стек технологий
2) Финансирование, работники
3) Целевая аудитория
4) Нефункциональные требования
5) Проблема
"""

class ChatRequest(BaseModel):
    messages: List[dict]

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        messages = request.messages
        if not messages or messages[0].get("role") != "system":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

        response = ask_llm(history=messages)
        return ChatResponse(response=response['message']['content'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


SYSTEM_PROMPT_TZ = """
Ты — опытный бизнес-аналитик. На основе всего нашего разговора составь структурированное техническое задание (ТЗ) для MVP стартапа.

Используй следующую структуру:
1. Описание проблемы и целевой аудитории
2. Ключевые функции MVP
3. Рекомендуемый стек технологий
4. Нефункциональные требования (производительность, безопасность)
5. Пользовательские сценарии
6. Критерии успеха
7. Оценка этапов и сроков (примерно)

Ответ должен быть подробным, на русском языке, в формате Markdown.
"""

@app.post("/api/generate_tz", response_model=ChatResponse)
async def generate_tz(request: ChatRequest):
    try:
        history = request.messages
        full_messages = [{"role": "system", "content": SYSTEM_PROMPT_TZ}] + history
        full_messages.append({"role": "user", "content": "Сформируй техническое задание на основе нашего диалога."})

        response = ask_llm(history=full_messages)
        return ChatResponse(response=response['message']['content'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return FileResponse("static/index.html")