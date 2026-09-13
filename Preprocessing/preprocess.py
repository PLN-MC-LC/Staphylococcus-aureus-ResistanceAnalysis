import os
import argparse
import json
from dotenv import load_dotenv
from utils_proprocess import (importar_arq, criar_pipeline,
                              preprocessar, criar_nome,
                              salvar_arquivo)
# carregar utils

load_dotenv()

PREPROCESSAMENTOS = ["case-folding", "stop-word-removal",
                     "stemming", "lemmatization"]


def main():
    parser = argparse.ArgumentParser(
        description="Processa artigos com diversos métodos",
        formatter_class=argparse.RawDesctiptionHelpFormatter,
        epilot="preprocess.py --arg1",
    )

    parser.add_argument(
        "preprocessamentos",
        nargs="*",
        choices=list(PREPROCESSAMENTOS),
        help="Preprocessamentos disponíveis",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do CSV de entrada.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Caminho do CSV de saída.",
    )

    parser.add_argument(
        "--abstract_column",
        required=True,
        help="Nome da coluna contendo o abstract.",
    )

    parser.add_argument(
        "--tokenizar",
        action="store_true",
        help="Indica se o texto deve ser tokenizado",
    )

    args = parser.parse_args()
    df = importar_arq(args.input, args.abstract_column)
    pipeline, nome_pipeline = criar_pipeline(args.preprocessamentos)
    resultado = preprocessar(pipeline, df, args.abstract_column)
    nome_arquivo = criar_nome(nome_pipeline)
    salvar_arquivo(nome_arquivo, resultado)
    print("Processamento finalizado, os seus arquivos estão salvos em...")


if __name__ == "__main__":
    main()
