class PromptTemplateCreator:


    def __init__(self):
        print()

    def create_prompt(self, template, question: str, references: list) -> tuple[str, str]:
        question = question.strip()

        t = Template('Hello $name')

        # Substitute values into the fields
        s = t.safe_substitute(name='Bob')
        print(s)  # Prints: Hello Bob

        s = t.safe_substitute()
        print(s)

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