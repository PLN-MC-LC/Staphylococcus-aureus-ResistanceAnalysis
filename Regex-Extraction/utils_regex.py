import regex as re
import pandas as pd
import spacy
import random

nlp = spacy.load('en_core_sci_sm')


def get_regex(diretorio, abstract_column_tok):
    properties = []
    antibiotics = []
    values = []

    doc = str(abstract_column_tok)

    for sentence in doc.sents:

        property = re.search(
            r'\b(?:susceptible|sensitive)\b',
            str(sentence),
            re.IGNORECASE
        )

        if property is not None:

            value = re.search(
                r"\d+(?:\.\d+)?\s*%",
                str(sentence)
            )

            if value is not None:

                antibiotic = re.search(
                    r"\b(?:to|against)\s+([A-Za-z]+(?:[- ][A-Za-z]+)*)",
                    str(sentence),
                    re.IGNORECASE
                )

                if antibiotic is not None:

                    properties.append(property[0])
                    antibiotics.append(antibiotic.group(1))
                    values.append(value[0])

    return properties, antibiotics, values, sentence


def verifica_regex(
    properties,
    antibiotics,
    values,
    sentence,
    abstract_indices,
    n
):
    dados = list(zip(
        properties,
        antibiotics,
        values,
        sentence,
        abstract_indices
    ))

    amostra = random.sample(
        dados,
        min(n, len(dados))
    )

    return amostra
