from typing import List

from fastapi import APIRouter
# from pydantic import UUID4

from middleware.controller.controller import SearchController

search_router = APIRouter(prefix="/api", tags=["Search"])

@search_router.get("/search/", response_model=dict)
def search(question: str):
    return SearchController.search(question)
