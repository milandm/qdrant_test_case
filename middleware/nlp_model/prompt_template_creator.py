from utils.utils import prepare_template
from qdrant_client.http.models import ScoredPoint

PROMPT_TEMPLATE = """
        You propose closest meaning sentences : $question

        Cite them in your answer.

        References:

        $references

        \nHow to cite a reference: This is a citation [1]. This one too [3]. And this is sentence with many citations [2][3].\nAnswer:
        """

class PromptTemplateCreator:


    def __init__(self):
        print()

    def create_similar_sentences_prompt(self, question:str, references_list: list[ScoredPoint]) -> tuple[str, str]:

        references_text = ""

        for i, reference in enumerate(references_list, start=1):
            text = reference.payload["text"].strip()
            references_text += f"\n[{i}]: {text}"

        key_value_to_change ={
            "question": question.strip(),
            "references": references_text,
        }

        prompt = prepare_template(PROMPT_TEMPLATE, key_value_to_change)

        return prompt, references_text