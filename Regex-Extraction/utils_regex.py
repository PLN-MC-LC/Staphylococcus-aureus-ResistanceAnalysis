import regex as re
import pandas as pd
import spacy
from utils_preprocess import (importar_arq)
import random as rd

nlp = spacy.load('en_core_sci_sm')


def get_regex(diretorio, abstract_column):

    properties = []
    antibiotics = []
    values = []
    sentences = []
    abstract_indices = []

    for abstract_index, abstract in enumerate(abstract_column):

        doc = nlp(str(abstract))

        for sentence in doc.sents:

            property = re.search(
                r'\b(?:susceptible|sensitive|resistant)\b',
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

                        properties.append(property.group(0))
                        antibiotics.append(antibiotic.group(1))
                        values.append(value.group(0))
                        sentences.append(str(sentence))
                        abstract_indices.append(abstract_index)

    return (
        properties,
        antibiotics,
        values,
        sentences,
        abstract_indices
    )

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

    amostra = rd.sample(
        dados,
        min(n, len(dados))
    )
    for propriedade, antibiotico, valor, sentença, i in amostra:
        print(f"No abstract {i}, foi {valor} {propriedade} a {antibiotico}")
        print(f"Sentença completa: {sentença}")
        print()
        print("------------------------------------------------------")
        print()

    return amostra
