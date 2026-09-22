import pandas as pd
import nltk
from nltk.corpus import stopwords
import scispacy
import spacy
import os

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_sci_sm")


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


def tokenizar(df, abstract_column):
    df[abstract_column] = df[abstract_column].astype(str).fillna("")
    df[abstract_column] = list(nlp.pipe(df[abstract_column]))
    return df


def case_folding(df, abstract_column):
    df[abstract_column] = df[abstract_column].astype(str).str.lower()
    return df


def stop_word_removal(df, abstract_column):
    df[abstract_column] = df[abstract_column].apply(
        lambda tokens: [token for token in tokens if token.text not in stop_words]
    )
    return df


def lemmatization(df, abstract_column):
    df[abstract_column] = [" ".join([token.lemma_ for token in doc]) for doc in df[abstract_column]]
    return df


def preprocessar(passos, df, abstract_column, tokenizar_flag=False):
    name = ""

    if "case-folding" in passos:
        df = case_folding(df, abstract_column)
        name += "cf-"

    if tokenizar_flag:
        df = tokenizar(df, abstract_column)
        name += "tok-"

    if "stop-word-removal" in passos:
        df = stop_word_removal(df, abstract_column)
        name += "swr-"

    if "lemmatization" in passos:
        df = lemmatization(df, abstract_column)
        name += "lm-"

    name += "processed.csv"

    return df, name

def salvar_arquivo(nome_arquivo, arquivo, output):
    caminho = os.path.join(output, nome_arquivo)
    arquivo.to_csv(
        caminho,
        index=False,
    )
    return
