import sys

sys.path.append("..")

from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor
from repository.qdrant_db_client import QdrantDbClient
from middleware.nlp_model.nlp_model import NlpModel


BOOK_FILENAME = "Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe"

SENTENCE_MIN_LENGTH = 2



class SearchEngine:


    def __init__(self, collection_name :str, nlp_model :NlpModel):
        self.model = nlp_model
        self.qdrant_client = QdrantDbClient(collection_name=collection_name, vector_params_size = self.model.VECTOR_PARAMS_SIZE)


    def build_prompt(self, question: str, references: list) -> tuple[str, str]:
        prompt = f"""
        You propose closest meaning sentences : '{question}'

        Cite them in your answer.

        References:
        """.strip()

        references_text = ""

        for i, reference in enumerate(references, start=1):
            text = reference.payload["text"].strip()
            references_text += f"\n[{i}]: {text}"

        prompt += (
                references_text
                + "\nHow to cite a reference: This is a citation [1]. This one too [3]. And this is sentence with many citations [2][3].\nAnswer:"
        )
        return prompt, references_text

    def ask(self,question: str) -> dict:
        question_embedding = self.model.get_embedding(question)

        similar_docs = self.qdrant_client.search_sentences(encoded_question = question_embedding)

        print(similar_docs)

        prompt, references = self.build_prompt(question, similar_docs)
        response = self.model.send_prompt(prompt)

        return {
            "response": response["choices"][0]["message"]["content"],
            "references": references,
        }