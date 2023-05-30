from middleware.services.recommendation_service import RecommendationService
from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor


from config import COLLECTION_NAME


if __name__ == "__main__":
    nlp_model = OpenaiSdkInterceptor()
    recommendation_service = RecommendationService(COLLECTION_NAME, nlp_model)
    print(recommendation_service.recommend_history_based())