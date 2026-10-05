import argparse
from utils_llm_analysis import (importar_json,
                                aplicar_cutoff,
                                plot_antibiotic_percentage,
                                plot_antibiotic_resistance,
                                tabela_antibioticos,
                                plot_antibiotic_cooccurrence)

ANALYSIS = ["antibiotic-per-property",
            "antibiotic-resistance",
            "antibiotic-counts",
            "antibiotic-cooccurrence"]


def main():
    parser = argparse.ArgumentParser(
        description="Analisa artigos com diversos métodos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="word_analysis.py [args]",
    )

    parser.add_argument(
        "analises",
        nargs="*",
        choices=list(ANALYSIS),
        help="Análises disponíveis",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do JSON de entrada.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Caminho de saída.",
    )

    parser.add_argument(
        "--extracoes_col",
        required=True,
        help="Nome da chave onde estão as extrações",
    )

    parser.add_argument(
        "--cutoff",
        help="Delimita quantas aparições um antibiótico deve ter",
    )

    args = parser.parse_args()
    print(args)
    df = aplicar_cutoff(importar_json(args.input, args.extracoes_col),
                        "antibiotic", int(args.cutoff))

    print(df.columns)

    print(
        df["antibiotic"]
        .value_counts()
        .sort_index()
    )

    if "antibiotic-per-property" in args.analises:
        plot_antibiotic_percentage(df, args.output)
    if "antibiotic-resistance" in args.analises:
        plot_antibiotic_resistance(df, args.output)
    if "antibiotic-counts" in args.analises:
        tabela_antibioticos(df, args.output)
    if "antibiotic-cooccurrence" in args.analises:
        plot_antibiotic_cooccurrence(
            df,
            coluna="antibiotic",
            grupo="abstract_id",
            output=args.output
        )


if __name__ == "__main__":
    main()
