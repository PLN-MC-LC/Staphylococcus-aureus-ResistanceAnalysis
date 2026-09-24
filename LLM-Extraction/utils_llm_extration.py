import re
import json
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


def perguntar(client, MODEL, TEMP, user, system=None, assistant=None):
    mensagens = []
    if system:
        mensagens.append({"role": "system", "content": system})
    if assistant:
        for assist, a_user in assistant:
            mensagens.append({"role": "assistant", "content": assist})
            mensagens.append({"role": "user", "content": a_user})
    mensagens.append({"role": "user", "content": user})

    resposta = client.chat.completions.create(model=MODEL, messages=mensagens,
                                              temperature=TEMP)
    
    return resposta.choices[0].message.content


def limpar_cercas(texto):
    t = texto.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)

    return t


def extrair_llm(resposta):
    try:
        return json.loads(limpar_cercas(resposta)).get("extrações", [])
    except json.JSONDecodeError:
        print("  (resposta não era JSON):", resposta[:120])
    return []


def testar_conexao(client, MODEL, TEMP):
    conexao = perguntar(client, MODEL,
                        TEMP, "Responda apenas: conexão OK.")

    if conexao:
        print(conexao)
        return True
    return False
