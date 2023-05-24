
from fastapi import HTTPException, Response
from middleware.search_engine import SearchEngine
from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor
from middleware.exceptions.search_exceptions import SearchExceptionCode
from config import COLLECTION_NAME

class SearchController:


    @staticmethod
    def search(question: str):
        try:
            nlp_model = OpenaiSdkInterceptor()
            search_engine = SearchEngine(COLLECTION_NAME, nlp_model)
            response = search_engine.ask(question)
            print(response)
            return response
        except SearchExceptionCode as e:
            print(e)
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

