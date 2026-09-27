import os
import argparse
from utils_word_processing import (importar_arq)

ANALYSIS = ["TF-IDF"]


def main():
    parser = argparse.ArgumentParser(
        description="Analisa artigos com diversos métodos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="word_analysis.py [args]",
    )

    parser.add_argument(
        "análises",
        nargs="*",
        choices=list(ANALYSIS),
        help="Análises disponíveis",
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

    args = parser.parse_args()
    df = importar_arq(args.input, args.abstract_column)
    print(df)


if __name__ == "__main__":
    main()
