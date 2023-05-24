from sentence_transformers import SentenceTransformer
import torch

import numpy as np
from numpy import ndarray
from tqdm import tqdm
from middleware.nlp_model.nlp_model import NlpModel
from typing import List, Dict, Tuple, Iterable, Type, Union, Callable, Optional, Generator, Any
from openai.openai_object import OpenAIObject
from middleware.nlp_model.openai_sdk_interceptor import OpenaiSdkInterceptor


SENTENCE_TRANSFORMER_NLP_MODEL = "msmarco-MiniLM-L-6-v3"
CUDA = "cuda"
MPS = "mps"
CPU = "cpu"

class SentenceTransformerInterceptor(NlpModel):

    VECTOR_PARAMS_SIZE = 384

    def __init__(self):
        self.model = SentenceTransformer(
            SENTENCE_TRANSFORMER_NLP_MODEL,
            device=CUDA
            if torch.cuda.is_available()
            else MPS
            if torch.backends.mps.is_available()
            else CPU,
        )
        self.nlp_prompt_model = OpenaiSdkInterceptor()

    def get_embeddings(self, sentences: list[str]) -> ndarray:

        vectors = []
        batch_size = 512
        batch = []

        for doc in tqdm(sentences):
            batch.append(doc)

            if len(batch) >= batch_size:
                vectors.append(self.model.encode(batch))
                batch = []

        if len(batch) > 0:
            vectors.append(self.model.encode(batch))
            batch = []

        vectors = np.concatenate(vectors)

        return vectors

    def get_embedding(self, text:str) -> Union[Generator[Union[list, OpenAIObject, dict], Any, None], list, OpenAIObject, dict]:
        self.model.encode(text)


    def send_prompt( self, prompt:str ) -> Union[Generator[Union[list, OpenAIObject, dict], Any, None], list, OpenAIObject, dict]:
        return self.nlp_prompt_model.send_prompt(prompt)