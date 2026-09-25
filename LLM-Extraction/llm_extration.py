import os
import argparse
import json
import time
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from utils_llm_extration import (importar_arq, testar_conexao, extrair_llm)
from prompts import (SYSTEM, ASSISTANT)

load_dotenv()

API_KEY = os.getenv("ILUMA_API_KEY")
BASE_URL = "https://iluma.cnpem.br:4000/v1"
MODEL = "iluma"
TEMP = 0.5
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

    parser.add_argument(
        "--limite",
        help="Num. limite de Abstracts a serem processados",
    )

    args = parser.parse_args()

    df = importar_arq(args.input, args.abstract_column)
    abstracts = df[args.abstract_column]
    SAIDA = Path(args.output)
    if args.limite:
        limite = int(args.limite)
    else:
        limite = None

    if testar_conexao(client, MODEL, TEMP):
        print("Conexão estabelecida")
        feitos = set()
        if SAIDA.exists():
            with SAIDA.open() as f:
                feitos = {json.loads(row)["i"] for row in f if row.strip()}
            print(f"{len(feitos)} itens já processados serão pulados")

        alvos = list(enumerate(abstracts))
        if limite:
            alvos = alvos[:limite]

        with SAIDA.open("a") as f:
            for i, abstract in alvos:
                print(abstract)
                if i in feitos:
                    continue
                try:
                    linha = {"i": i, "extracoes": extrair_llm(client,
                                                              MODEL,
                                                              TEMP,
                                                              abstract,
                                                              SYSTEM,
                                                              ASSISTANT,
                                                              i)}
                except Exception as e:
                    linha = {"i": i, "erro": f"{type(e).__name__}: {e}"}
                    print(f"  [{i}] falhou: {type(e).__name__}")
                f.write(json.dumps(linha, ensure_ascii=False) + "\n")
                f.flush()
                time.sleep(0.2)
        print("Fim")
    else:
        print("Não há conexão com a ILUMA")
        return False
    return True


if __name__ == "__main__":
    main()
