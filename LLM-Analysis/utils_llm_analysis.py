import pandas as pd
import json
import matplotlib.pyplot as plt
import os
import numpy as np
import itertools
import seaborn as sns
from antibiotic_normalization import ANTIBIOTIC_NORMALIZATION


plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "axes.titlesize": 18
})


def importar_json(arquivo, chave):

    registros = []
    vazios = 0
    erros = []

    with open(arquivo, "r", encoding="utf-8") as f:
        for i, linha in enumerate(f):
            if not linha.strip():
                continue

            dados = json.loads(linha)

            if "erro" in dados:
                erros.append(dados)
                continue

            extracoes = dados.get(chave, [])

            if extracoes == []:
                vazios += 1

            elif isinstance(extracoes, list):
                for extracao in extracoes:
                    extracao["abstract_id"] = i
                    registros.append(extracao)

    df = pd.DataFrame(registros)

    print(f"Valores vazios: {vazios}")
    print(f"Valores com erro: {len(erros)}")
    print(f"Total de problemas: {vazios + len(erros)}")

    if erros:
        print("\nErros:")
        for erro in erros:
            print(f"  i={erro.get('i')}: {erro.get('erro')}")

    print(f"# de extrações: {df.shape[0]}")

    df["antibiotic"] = df["antibiotic"].apply(normalize_antibiotic)

    return df


def normalize_antibiotic(value):
    if pd.isna(value):
        return value

    value = str(value).strip().lower()

    return ANTIBIOTIC_NORMALIZATION.get(value, value)


def aplicar_cutoff(df, coluna, cutoff):
    counts = df[coluna].value_counts()
    valores_validos = counts[counts >= cutoff].index

    return df[df[coluna].isin(valores_validos)].copy()


def plot_antibiotic_percentage(df, output):

    dados = (
        df.groupby(["antibiotic", "property"])
        .size()
        .reset_index(name="count")
    )

    dados["percentage"] = (
        dados["count"]
        / dados.groupby("antibiotic")["count"].transform("sum")
        * 100
    )

    dados = dados.pivot(
        index="antibiotic",
        columns="property",
        values="percentage"
    ).fillna(0)

    dados = dados.sort_values("resistant")

    fig, ax = plt.subplots(figsize=(10, 10))

    y = np.arange(len(dados))

    ax.barh(
        y,
        dados["resistant"],
        label="Resistant",
        color="#1A1A1A"
    )

    ax.barh(
        y,
        dados["sensitive"],
        left=dados["resistant"],
        label="Sensitive",
        color="#FF6B99"
    )

    ax.set_yticks(y)
    ax.set_yticklabels(dados.index)

    ax.set_xlabel("Percentage of appearances (%)")
    ax.set_ylabel("Antibiotic")

    ax.set_xlim(0, 100)

    ax.legend(
        loc="lower right"
    )

    fig.tight_layout()

    path = os.path.join(
        output,
        "antibioticXpercentage.pdf"
    )

    fig.savefig(
        path,
        format="pdf",
        bbox_inches="tight"
    )

    plt.close(fig)


def plot_antibiotic_resistance(df, output):

    dados = (
        df.groupby(["antibiotic", "property"])["percentage"]
        .mean()
        .reset_index()
    )

    dados = dados.pivot(
        index="antibiotic",
        columns="property",
        values="percentage"
    )

    dados = dados.sort_values("resistant")

    fig, ax = plt.subplots(figsize=(10, 10))

    y = np.arange(len(dados))
    width = 0.35

    ax.barh(
        y - width / 2,
        dados["resistant"],
        height=width,
        label="Resistant",
        color="#1A1A1A"
    )

    ax.barh(
        y + width / 2,
        dados["sensitive"],
        height=width,
        label="Sensitive",
        color="#FF6B99"
    )

    ax.set_yticks(y)
    ax.set_yticklabels(dados.index)

    ax.set_xlabel("Percentage (%)")
    ax.set_ylabel("Antibiotic")

    ax.set_xlim(0, 100)

    ax.legend(
        loc="lower right"
    )

    fig.tight_layout()

    path = os.path.join(
        output,
        "antibioticXresistance.pdf"
    )

    fig.savefig(
        path,
        format="pdf",
        bbox_inches="tight"
    )

    plt.close(fig)


def tabela_antibioticos(df, output):

    tabela = (
        df["antibiotic"]
        .value_counts()
        .rename_axis("antibiotic")
        .reset_index(name="count")
    )

    path = os.path.join(
        output,
        "antibiotic_counts.csv"
    )

    tabela.to_csv(
        path,
        index=False
    )

    return tabela


def plot_antibiotic_cooccurrence(df, coluna, grupo, output):

    presenca = pd.crosstab(df[grupo], df[coluna]).clip(upper=1)
    presenca = presenca.reindex(sorted(presenca.columns), axis=1)

    contagens = presenca.T.dot(presenca)
    n_abs = np.diag(contagens.values).astype(float)

    uniao = n_abs[:, None] + n_abs[None, :] - contagens.values
    matriz = pd.DataFrame(
        contagens.values / uniao,
        index=contagens.index,
        columns=contagens.columns,
    )

    mask = np.triu(np.ones_like(matriz, dtype=bool))

    plt.figure(figsize=(16, 14))

    sns.heatmap(
        matriz,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="cividis",
        linewidths=0.5,
        linecolor="white",
        annot_kws={"fontsize": 7},
        cbar_kws={"label": "Jaccard index"},
    )

    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    plt.xlabel("Antibiotic")
    plt.ylabel("Antibiotic")

    path = os.path.join(
        output,
        "cooccurrence.pdf"
    )

    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
