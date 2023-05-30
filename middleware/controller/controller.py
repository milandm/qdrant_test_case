
from fastapi import HTTPException, Response
from middleware.search_service import SearchService
from middleware.recommendation_service import RecommendationService
from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor
from middleware.exceptions.search_exceptions import SearchExceptionCode
from middleware.exceptions.recommendation_exception import RecommendationExceptionCode
from config import COLLECTION_NAME

class Controller:


    @staticmethod
    def search(question: str):
        try:
            nlp_model = OpenaiSdkInterceptor()
            search_service = SearchService(COLLECTION_NAME, nlp_model)
            response = search_service.search(question)
            print(response)
            return response
        except SearchExceptionCode as e:
            print(e)
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    @staticmethod
    def recommend_history_based():
        try:
            nlp_model = OpenaiSdkInterceptor()
            recommendation_service = RecommendationService(COLLECTION_NAME, nlp_model)
            response = recommendation_service.recommend_history_based()
            print(response)
            return response
        except RecommendationExceptionCode as e:
            print(e)
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

