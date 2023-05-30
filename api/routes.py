from typing import List

from fastapi import APIRouter
# from pydantic import UUID4

from middleware.controller.controller import Controller

search_router = APIRouter(prefix="/api", tags=["Search"])

@search_router.get("/search/", response_model=dict)
def search(question: str):
    return Controller.search(question)

@search_router.get("/recommend_history_based", response_model=dict)
def search():
    return Controller.recommend_history_based()