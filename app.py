import os
from typing import List, Optional, Union
from pydantic import BaseModel
from fastapi import FastAPI, Request
from typing import Optional, List, Dict
from src.vector_updation import url_data_updation, load_store
from src.chat import chat
import json
import uvicorn


vector_store = load_store()


class BaseChatRequestType(BaseModel):
    user_id: str
    messages: Optional[List[Dict]] = [{}]


class BaseUrlRequestType(BaseModel):
    urls: List[str]
    user_id: str


app = FastAPI(title="RAG-Link-api")


@app.get("/health")
async def health(request: Request):
    return "Server up and running"


@app.post("/api/v1/index")
async def index(data: BaseUrlRequestType, request: Request):
    if type(data.urls) != list or type(data.user_id) != str:
        return json.dumps(
            {
                "error": "Please provide correct format for urls(List[str]) and user_id(str)"
            }
        )

    return json.dumps(url_data_updation(data.urls, data.user_id, vector_store))


@app.post("/api/v1/chat")
async def websocket_endpoint(data: BaseChatRequestType, request: Request):
    if type(data.messages) != list or type(data.user_id) != str:
        return json.dumps(
            {
                "error": "Please provide correct format for urls(List[str]) and user_id(str)"
            }
        )
    try:
        response = chat(data.messages, data.user_id, vector_store)
        return json.dumps(response)
    except Exception as e:
        return json.dumps(
            {"error": "Error while sending request", "Error_type": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
