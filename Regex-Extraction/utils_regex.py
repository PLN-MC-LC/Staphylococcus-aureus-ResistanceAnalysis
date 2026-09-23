import regex as re
import pandas as pd
import spacy
import random as rd

nlp = spacy.load('en_core_sci_sm')


def importar_arq(diretorio, abstract_column):
    try:
        df = pd.read_csv(diretorio)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Arquivo não encontrado: {diretorio}"
        )

    if abstract_column not in df.columns:
        raise ValueError(
            f"A coluna '{abstract_column}' não existe no CSV.\n"
            f"Colunas disponíveis: {list(df.columns)}"
        )

    return df


def get_regex(abstract_column_tok):
    properties = []
    antibiotics = []
    values = []
    sentences = []
    abstract_indices = []
    
    i = -1
    for abstract in abstract_column_tok:
        i += 1 
        doc = nlp(str(abstract))

        for sentence in doc.sents:

            property = re.search(
                r'\b(?:susceptible|sensitive|resistant|resistance)\b',
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
                        abstract_indices.append(i)

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

def make_df_regex(df, abstract_indices):
    df_regex = df.iloc[abstract_indices].copy()
    return df_regex
