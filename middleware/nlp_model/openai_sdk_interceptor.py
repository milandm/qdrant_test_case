import openai

from typing import List, Dict, Tuple, Iterable, Type, Union, Callable, Optional, Generator, Any
from openai.openai_object import OpenAIObject
from middleware.nlp_model.nlp_model import NlpModel

import numpy as np
from numpy import ndarray
from tqdm import tqdm

from config import (
    COLLECTION_NAME,
    OPENAI_API_KEY,
    QDRANT_API_KEY,
    QDRANT_HOST,
    QDRANT_PORT,
)

OPENAI_NLP_MODEL = "text-embedding-ada-002"

class OpenaiSdkInterceptor(NlpModel):

    VECTOR_PARAMS_SIZE = 1536

    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def send_prompt( self, prompt:str ) -> Union[Generator[Union[list, OpenAIObject, dict], Any, None], list, OpenAIObject, dict]:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=250,
            temperature=0.2,
        )
        return response

        # return {
        #     "response": response["choices"][0]["message"]["content"],
        #     "references": references,
        # }



    def get_embedding(self, text) -> Union[Generator[Union[list, OpenAIObject, dict], Any, None], list, OpenAIObject, dict]:
        # text = text.replace("\n", " ")

        if isinstance(text, str):
            text = [text]
        embedding = openai.Embedding.create(input=text, model=OPENAI_NLP_MODEL)
        # return embedding['data'][0]['embedding']

        embeddings = [row["embedding"]
            for row in embedding['data']
        ]

        if len(embeddings) == 1:
            return embeddings[0]

        return embeddings

        # df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
        # df.to_csv('output/embedded_1k_reviews.csv', index=False)

        # import pandas as pd
        #
        # df = pd.read_csv('output/embedded_1k_reviews.csv')
        # df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)

    def get_embeddings(self, sentences: list[str]) -> ndarray:
        vectors = []
        batch_size = 512
        batch = []

        for doc in tqdm(sentences):
            batch.append(doc)

            if len(batch) >= batch_size:
                vectors.append(self.get_embedding(batch))
                batch = []

        if len(batch) > 0:
            vectors.append(self.get_embedding(batch))
            batch = []

        vectors = np.concatenate(vectors)

        return vectors