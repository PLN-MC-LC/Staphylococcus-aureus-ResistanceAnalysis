import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("ILUMA_API_KEY")
BASE_URL = "https://iluma.cnpem.br:4000/v1"
MODELO = "iluma"
TEMP_EXTRACAO = 0.5

cliente = OpenAI(base_url=BASE_URL, api_key=API_KEY,
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

    return
