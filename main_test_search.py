from middleware.search_engine import SearchEngine
from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor


from config import COLLECTION_NAME


if __name__ == "__main__":
    nlp_model = OpenaiSdkInterceptor()
    search_engine = SearchEngine(COLLECTION_NAME, nlp_model)
    print(search_engine.ask("Dog eats bone"))