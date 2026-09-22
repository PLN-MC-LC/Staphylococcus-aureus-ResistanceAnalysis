import re
import json


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
                                              temperatura=TEMP)
    return resposta


def limpar_cercas(texto):
    t = texto.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    return


def extrair_llm(resposta):
    try:
        return json.loads(limpar_cercas(resposta)).get("extrações", [])
    except json.JSONDecodeError:
        print("  (resposta não era JSON):", resposta[:120])
    return []
