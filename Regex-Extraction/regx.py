from utils_preprocess import (importar_arq)
from utils_regex import get_regex, verifica_regex
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Processa Abstracts usando regras regex.",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do CSV de entrada"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Caminho do CSV de entrada"
    )

    parser.add_argument(
        "--abstract_column",
        required=True,
        help="Coluna que contém os abstracts",
    )

    args = parser.parse_args()

    df = importar_arq(args.input, args.abstract_column)

    props, antibiotics, values, sentence = get_regex(df, args.abstract_column)
    verifica_regex(props, antibiotics, values, sentence)
    return
