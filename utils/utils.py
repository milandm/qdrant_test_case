import json
from string import Template
from collections import defaultdict

@staticmethod
def load_file(file_name: str):
    with open(file_name, "r") as file:
        meditations_json = json.load(file)
        return meditations_json

@staticmethod
def prepare_template(template: str, key_value_to_change:dict) -> str:
    prompt_template = Template(template)
    try:
        prepared_prompt = prompt_template.safe_substitute(key_value_to_change)
    except KeyError as e:
        print(e)
    except ValueError as e:
        print(e)

    # mapping = defaultdict(str, key_value_to_change)
    # prepared_prompt = template.format_map(mapping=mapping)
    return prepared_prompt


@staticmethod
def is_close(a, b, threshold):
    return abs(a - b) <= threshold