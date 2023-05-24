import sys

sys.path.append("..")

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from config import DATA


def split_with_delimiter(text: str, delim: str) -> list:
    split_sentences = re.split(f"({delim})", text)
    combined_sentences: list = []
    for i in range(0, len(split_sentences)):
        if split_sentences[i] == ".":
            combined_sentences[-1] += split_sentences[i]
        else:
            combined_sentences.append(split_sentences[i])
    return combined_sentences


def clean_text(text: str) -> str:
    clean_text = text.encode("ascii", "ignore").decode("utf-8")
    clean_text = re.sub(r" {2,}", " ", clean_text)
    clean_text = re.sub(r" \n", "\n", clean_text)
    clean_text = re.sub(r"\n ", "\n", clean_text).strip()
    return clean_text


def extract_text_from_html(
    book: str,
    book_name: str,
    max_sentence_length: int = 100,
) -> None:
    file = DATA / "unzipped" / book / "index.html"
    output_folder = DATA / "processed" / book

    Path(output_folder).mkdir(parents=True, exist_ok=True)

    with open(file, "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    data = []
    excluded_sections = ["GLOSSARY", "NOTES", "APPENDIX", "INTRODUCTION"]

    for section in soup.select("section"):
        if (
            section.find("h2")
            and section.find("h2").get_text().strip() not in excluded_sections
        ):
            section_title = section.find("h2").get_text()
            section_text = ""

            for t in section.select("p"):
                for elem_to_remove in (
                    t.select("[class='calibre24']")
                    + t.select("[class='mw-ref']")
                    + t.select("[class='reference']")
                ):
                    elem_to_remove.decompose()
                section_text += "\n" + t.get_text()

            section_text = clean_text(section_text)

            fixed_length_sentences = []

            for paragraph in section_text.split("\n"):
                if len(paragraph.split()) > max_sentence_length:
                    sentences = split_with_delimiter(paragraph, "\.")
                    current_sentence = ""

                    for i in range(len(sentences)):
                        if (
                            len(current_sentence.split()) + len(sentences[i].split())
                            < max_sentence_length
                        ):
                            current_sentence += sentences[i]
                        else:
                            fixed_length_sentences.append(current_sentence)
                            current_sentence = sentences[i]
                else:
                    fixed_length_sentences.append(paragraph)

            data.append(
                {
                    "title": section_title,
                    "url": f"https://en.wikisource.org/wiki/{book}#{'_'.join(section_title.split())}",
                    "sentences": fixed_length_sentences,
                }
            )

    output = {
        "book_title": book_name,
        "url": f"https://en.wikisource.org/wiki/{book}",
        "data": data,
    }

    json.dump(output, open(output_folder / f"{book}.json", "w"), indent=4)
    print(f"Saved {book}.json with content of book.")

extract_text_from_html(
    "Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe",
    "Meditations by Marcus Aurelius",
)