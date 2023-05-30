from middleware.services.search_service import SearchService
from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor


from config import COLLECTION_NAME


if __name__ == "__main__":
    nlp_model = OpenaiSdkInterceptor()
    search_service = SearchService(COLLECTION_NAME, nlp_model)
    print(search_service.search("Cow eats bone"))