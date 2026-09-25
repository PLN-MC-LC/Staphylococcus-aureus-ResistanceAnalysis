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


def testar_conexao(client, MODEL, TEMP):
    conexao = perguntar(client, MODEL,
                        TEMP, "Responda apenas: conexão OK.")

    if conexao:
        print(conexao)
        return True
    return False


def perguntar(client, MODEL, TEMP, user, system=None, assistant=None,
              json_mode=False, max_tokens=16000):
    mensagens = []
    if system:
        mensagens.append({"role": "system", "content": system})
    if assistant:
        for assist, a_user in assistant:
            mensagens.append({"role": "assistant", "content": assist})
            mensagens.append({"role": "user", "content": a_user})
    mensagens.append({"role": "user", "content": user})

    extra = {"response_format": {"type": "json_object"}} if json_mode else {}

    resposta = client.chat.completions.create(model=MODEL,
                                              messages=mensagens,
                                              max_tokens=max_tokens,
                                              temperature=TEMP,
                                              **extra)
    msg = resposta.choices[0].message
    finish = resposta.choices[0].finish_reason

    return msg.content, getattr(msg, "reasoning", None), finish


def limpar_cercas(texto):
    t = texto.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)

    return t


def ler_json(resposta):
    t = limpar_cercas(resposta)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", t, re.S)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
        print("  (resposta não era JSON):", t[:120])
    return {}


def extrair_llm(client, MODEL, TEMP, abstract,
                SYSTEM=None, ASSISTANT=None, i=None):
    resposta, raciocinio, motivo = perguntar(client, MODEL, TEMP,
                                             abstract, SYSTEM,
                                             ASSISTANT, json_mode=True)
    print(f"[{i}] raciocinio: {raciocinio}, motivo: {motivo}")
    json_limpo = ler_json(resposta)
    return json_limpo.get("extracoes", [])
