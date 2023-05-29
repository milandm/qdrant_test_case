import sys

sys.path.append("..")

import json

import numpy as np
import pandas as pd
import torch

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor
from middleware.nlp_model.sentence_transformer_interceptor import SentenceTransformerInterceptor

from tqdm import tqdm

from config import QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY, DATA, COLLECTION_NAME
from repository.qdrant_db_client import QdrantDbClient
from middleware.nlp_model.nlp_model import NlpModel

BOOK_FILENAME = "Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe"

# SENTENCE_MIN_LENGTH = 15
SENTENCE_MIN_LENGTH = 2

class VectorizeTextEngine:


    def __init__(self, collection_name :str, nlp_model :NlpModel):
        self.model = nlp_model
        self.client = QdrantDbClient(collection_name=collection_name, vector_params_size = self.model.VECTOR_PARAMS_SIZE)
        self.client.recreate_collection()


    def load_file(self):
        with open(f"{DATA}/processed/{BOOK_FILENAME}/{BOOK_FILENAME}.json", "r") as file:
            self.meditations_json = json.load(file)

    def read_sentences(self):

        rows = []
        for chapter in tqdm(self.meditations_json["data"]):
            for sentence in chapter["sentences"]:
                rows.append(
                    (
                        chapter["title"],
                        chapter["url"],
                        sentence,
                    )
                )

        df = pd.DataFrame(data=rows, columns=["title", "url", "sentence"])

        self.df = df[df["sentence"].str.split().str.len() > SENTENCE_MIN_LENGTH]

    def vectorize_sentences(self):

        vectors = []
        batch_size = 512
        batch = []

        for doc in tqdm(self.df["sentence"].to_list()):
            batch.append(doc)

            if len(batch) >= batch_size:
                vectors.append(self.model.get_embeddings(batch))
                batch = []

        if len(batch) > 0:
            vectors.append(self.model.get_embeddings(batch))
            batch = []

        self.vectors = np.concatenate(vectors)
        self.book_name = self.meditations_json["book_title"]


    def upsert_sentences(self):

        ids=[i for i in range(self.df.shape[0])],
        payloads=[
            {
                "text": row["sentence"],
                "title": row["title"] + f", {self.book_name}",
                "url": row["url"],
            }
            for _, row in self.df.iterrows()
        ],
        vectors=[v.tolist() for v in self.vectors]

        self.client.upsert_sentences(ids,  payloads, vectors)





