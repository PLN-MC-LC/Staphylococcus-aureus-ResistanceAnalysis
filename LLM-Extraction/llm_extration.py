import os
import argparse
# import json
from dotenv import load_dotenv
from openai import OpenAI
from utils_llm_extration import (testar_conexao, perguntar, extrair_llm,
                                 importar_arq)
from prompts import (SYSTEM, ASSISTANT)

load_dotenv()

API_KEY = os.getenv("ILUMA_API_KEY")
BASE_URL = "https://iluma.cnpem.br:4000/v1"
MODEL = "iluma"
TEMP_EXT = 0.5
TIMEOUT_SECS = 500

client = OpenAI(base_url=BASE_URL, api_key=API_KEY,
                timeout=TIMEOUT_SECS, max_retries=1)


def main():
    parser = argparse.ArgumentParser(
        description="Extrai dados usando a LLM Iluma (modelo QWEN).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="llm_extraction.py",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do CSV de entrada.",
    )

    parser.add_argument(
        "--abstract_column",
        required=True,
        help="Nome da coluna que contém o abstract",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Caminho do JSON de saída.",
    )

    args = parser.parse_args()

    df = importar_arq(args.input, args.abstract_column)

    if testar_conexao(client, MODEL, TEMP_EXT):
        json_extracted = []
        for abstract in df[args.abstract_column]:
            resposta = perguntar(client, MODEL, TEMP_EXT,
                                 abstract, SYSTEM)
            json_limpo = extrair_llm(resposta)
            print(json_limpo)
            json_extracted.append(json_limpo)
    else:
        print("Não há conexão com a ILUMA")
        return False
    print(json_extracted)
    return True


if __name__ == "__main__":
    main()
