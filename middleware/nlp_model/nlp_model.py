from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Iterable, Type, Union, Callable, Optional, Generator, Any
from openai.openai_object import OpenAIObject
from numpy import ndarray

class NlpModel(ABC):

    VECTOR_PARAMS_SIZE = 384
    # VECTOR_PARAMS_SIZE = 1536

    @abstractmethod
    def get_embeddings(self, sentences: Union[str, list[str]]) -> ndarray:
        pass

    @abstractmethod
    def get_embedding(self, text:str) -> Union[Generator[Union[list, OpenAIObject, dict], Any, None], list, OpenAIObject, dict]:
        pass

    @abstractmethod
    def send_prompt( self, prompt:str ) -> Union[Generator[Union[list, OpenAIObject, dict], Any, None], list, OpenAIObject, dict]:
        pass