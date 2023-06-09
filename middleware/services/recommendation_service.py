import sys

sys.path.append("..")

from repository.qdrant_db_client import QdrantDbClient
from middleware.nlp_model.nlp_model import NlpModel
from middleware.nlp_model.prompt_template_creator import PromptTemplateCreator



BOOK_FILENAME = "Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe"

SENTENCE_MIN_LENGTH = 2



class RecommendationService:


    def __init__(self, collection_name :str, nlp_model :NlpModel):
        self.model = nlp_model
        self.qdrant_client = QdrantDbClient(collection_name=collection_name, vector_params_size = self.model.VECTOR_PARAMS_SIZE)
        self.prompt_template_creator = PromptTemplateCreator()

    def recommend_history_based(self) -> dict:
        filtered_sentences = self.qdrant_client.query_payloads_filtered_sentences(
                                                                    query_filter_key = "data_type",
                                                                    query_filter_value = "question")

        positive_queries_ids = [item.id for item in filtered_sentences[0]]
        similar_docs = self.qdrant_client.recommend_sentences(positive_queries_ids = positive_queries_ids)

        print(filtered_sentences[0])

        prompt, references = self.prompt_template_creator.create_recommended_sentences_prompt(filtered_sentences[0], similar_docs)
        response = self.model.send_prompt(prompt)

        return {
            "response": response["choices"][0]["message"]["content"],
            "references": references,
        }