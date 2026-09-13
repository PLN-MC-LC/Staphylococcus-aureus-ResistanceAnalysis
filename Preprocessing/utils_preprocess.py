import pandas as pd
import nltk
from nltk.corpus import stopwords
import scispacy
import spacy

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_sci_sm")


def importar_arq(diretorio, abstract_column):
    try:
        df = pd.from_csv(diretorio)
    except FileNotFoundError:
        print("Arquivo não encontrado")

    if abstract_column not in df.columns:
        raise ValueError(
            f"A coluna '{abstract_column}' não existe no CSV. \n"
            f"Colunas disponíveis: '{list(df.columns)}'"
        )

    return df


def tokenizar(df, abstract_column):
    df[abstract_column] = df[abstract_column].astype(str).fillna("")
    df[abstract_column] = list(nlp.pipe(df[abstract_column]))
    return df


def case_folding(df, abstract_column):
    return df[abstract_column].str.lower()


def stop_word_removal(df, abstract_column):
    df[abstract_column] = df[abstract_column].apply(lambda tokens:[token for token in tokens if token not in stop_words])
    return df


def stemming(df, abstract_column):
    #TODO: implement
    return


def lemmatization(df, abstract_column):
    #TODO: implement
    return


def criar_pipeline(preprocessamento):
    print("TODO")
    pipeline = "a"
    nome_pipeline = "a"
    return pipeline, nome_pipeline


def preprocessar(pipeline, arquivo):
    df = "a"
    return df


def criar_nome(nome_pipeline):
    return


def salvar_arquivo(nome_arquivo, arquivo):
    return
