import os
import argparse
import json
from dotenv import load_dotenv
from utils_preprocess import (importar_arq, preprocessar, 
                              salvar_arquivo)
# carregar utils

load_dotenv()

PREPROCESSAMENTOS = ["case-folding", "stop-word-removal",
                     "lemmatization"]


def main():
    parser = argparse.ArgumentParser(
        description="Processa artigos com diversos mï¿½todos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="preprocess.py [args]",
    )

    parser.add_argument(
        "preprocessamentos",
        nargs="*",
        choices=list(PREPROCESSAMENTOS),
        help="Preprocessamentos disponï¿½veis",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do CSV de entrada.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Caminho do CSV de saï¿½da.",
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
    
    if args.preprocessamentos:
        passos = args.preprocessamentos

        resultado, arquivo = preprocessar(
            passos,
            df,
            args.abstract_column,
            args.tokenizar
        )
        
        salvar_arquivo(arquivo, resultado, args.output)
        print("Processamento finalizado!")
        print(f"Seu arquivo está salvo em {args.output}")
    
    else:
        print("Você deve selecionar pelo menos um pré-processamento.")


if __name__ == "__main__":
    main()
