import pandas as pd


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
