import sys

sys.path.append("..")

from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, DATA, COLLECTION_NAME
from middleware.nlp_model.nlp_model import NlpModel
import pandas as pd

BOOK_FILENAME = "Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe"

# SENTENCE_MIN_LENGTH = 15
SENTENCE_MIN_LENGTH = 2


class QdrantDbClient:

    def __init__(self, collection_name: str, vector_params_size: int):
        self.collection_name = collection_name
        self.vector_params_size = vector_params_size
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)


    def recreate_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=self.vector_params_size, distance=models.Distance.COSINE),
        )

    def search_sentences(self, encoded_question: str):
        similar_docs = self.client.search(
            collection_name=self.collection_name,
            query_vector=encoded_question,
            limit=3,
            append_payload=True,
        )
        return similar_docs


    def upsert_sentences(self, book_name: str, vectors: str, df: pd.DataFrame):
        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=[i for i in range(df.shape[0])],
                payloads=[
                    {
                        "text": row["sentence"],
                        "title": row["title"] + f", {book_name}",
                        "url": row["url"],
                    }
                    for _, row in df.iterrows()
                ],
                vectors=[v.tolist() for v in vectors],
            ),
        )