import sys

sys.path.append("..")

from qdrant_client import QdrantClient
from config import QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, DATA, COLLECTION_NAME
from qdrant_client.conversions import common_types as types
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, ScoredPoint

from qdrant_client.http import models
from numpy import ndarray
from typing import (
    Sequence,
    Union,
)

BOOK_FILENAME = "Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe"

# SENTENCE_MIN_LENGTH = 15
SENTENCE_MIN_LENGTH = 2
SENTENCES_RETURN_COUNT_LIMIT = 3

import uuid


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

    def search_sentences(self, encoded_question: str) ->  list[ScoredPoint]:
        similar_docs = self.client.search(
            collection_name=self.collection_name,
            query_vector=encoded_question,
            limit=SENTENCES_RETURN_COUNT_LIMIT,
            append_payload=True,
        )
        return similar_docs


    def upsert_sentences(self, payloads : list, vectors : list):

        ids=[uuid.uuid4().urn for i in range(len(payloads))]

        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=ids,
                payloads=payloads,
                vectors=vectors,
            ),
        )


    def recommend_sentences(self, positive_queries_ids: str) ->  list[ScoredPoint]:
        recommended_docs = self.client.recommend(
            collection_name=self.collection_name,
            positive=positive_queries_ids,
            limit=SENTENCES_RETURN_COUNT_LIMIT,
            with_payload=True,
        )
        return recommended_docs


    def query_payloads_filtered_sentences(self,query_filter_key: str,
                                            query_filter_value: str) ->  list[ScoredPoint]:


        query_filter = Filter(
            must=[
                FieldCondition(
                    key=query_filter_key,
                    match=models.MatchAny(value=query_filter_value)
                )
            ]
        )

        similar_docs = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=query_filter,
            limit=SENTENCES_RETURN_COUNT_LIMIT,
            with_payload=True,
        )
        return similar_docs


    def search_filtered_sentences(self, query_vector:Union[ndarray,
                                                           Sequence[float],
                                                           tuple[str, list[float]],
                                                           types.NamedVector],
                                  must_have_or_must_not_have: bool,
                                  query_filter_key: str,
                                  query_filter_value: str) ->  list[ScoredPoint]:

        if must_have_or_must_not_have:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key=query_filter_key,
                        match=MatchValue(value=query_filter_value)
                    )
                ]
            )
        else:
            query_filter = Filter(
                must_not=[
                    FieldCondition(
                        key=query_filter_key,
                        match=MatchValue(value=query_filter_value)
                    )
                ]
            )

        similar_docs = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=SENTENCES_RETURN_COUNT_LIMIT,
            append_payload=True,
        )
        return similar_docs