from middleware.vectorize_text_engine import VectorizeTextEngine
from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor

from config import COLLECTION_NAME


if __name__ == "__main__":
    nlp_model = OpenaiSdkInterceptor()
    vectorize_text = VectorizeTextEngine(COLLECTION_NAME, nlp_model)
    vectorize_text.load_file()
    vectorize_text.read_sentences()
    vectorize_text.vectorize_sentences()
    vectorize_text.upsert_sentences()