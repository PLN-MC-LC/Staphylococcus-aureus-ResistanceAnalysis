import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from utils_preprocess import (importar_arq)
from utils_llm_extraction import (perguntar, extrair_llm)
from prompts import (SYSTEM, ASSISTANT)

load_dotenv()

API_KEY = os.getenv("ILUMA_API_KEY")
BASE_URL = "https://iluma.cnpem.br:4000/v1"
MODEL = "iluma"
TEMP_EXTRACAO = 0.5

client = OpenAI(base_url=BASE_URL, api_key=API_KEY,
                timeout=60.0, max_retries=1)


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

    jsons_extracted = []

    for abstract in df[args.abstract_column]:
        user = abstract
        resposta = perguntar(client, MODEL,
                             TEMP_EXTRACAO, user,
                             SYSTEM, ASSISTANT)
        json_ext = extrair_llm(resposta)
        jsons_extracted.append(json_ext)

    path = os.path.join(args.output, "extracao.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(jsons_extracted, file, indent=4)
        print(f"Sua extração está disponível em: {path}!")
    return
