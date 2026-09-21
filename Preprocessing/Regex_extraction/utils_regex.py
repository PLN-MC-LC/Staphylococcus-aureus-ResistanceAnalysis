import regex as re
import pandas as pd
import spacy
from utils_preprocess import (importar_arq)

nlp = spacy.load('en_core_sci_sm')


def get_regex(diretorio, abstract_column):
    properties = []
    antibiotics = []
    values = []

    doc = nlp(str(abstract_column))

    for sentence in doc.sents:

        property = re.search(
            r'\b(?:susceptible|sensitive)\b',
            str(sentence),
            re.IGNORECASE
        )

        if property != None:

            value = re.search(
                r"\d+(?:\.\d+)?\s*%",
                str(sentence)
            )

            if value != None:

                antibiotic = re.search(
                    r"\b(?:to|against)\s+([A-Za-z]+(?:[- ][A-Za-z]+)*)",
                    str(sentence),
                    re.IGNORECASE
                )

                if antibiotic != None:

                    properties.append(property[0])
                    antibiotics.append(antibiotic.group(1))
                    values.append(value[0])

    return properties, antibiotics, values, sentence

import random

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