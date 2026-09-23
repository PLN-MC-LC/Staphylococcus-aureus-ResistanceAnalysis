from utils_regex import get_regex, verifica_regex, make_df_regex, importar_arq
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
        description="Processa Abstracts usando regras regex.",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do CSV de entrada"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Caminho do CSV de entrada"
    )

    parser.add_argument(
        "--abstract_column",
        required=True,
        help="Coluna que contém os abstracts. Eles devem estar tokenizados",
    )

    args = parser.parse_args()

    df = importar_arq(args.input, args.abstract_column)

    props, antibiotics, values, sentences, abstract_indices = get_regex(df[args.abstract_column])
    verifica_regex(props, antibiotics, values, sentences, abstract_indices, 10)
    df_regex = make_df_regex(df, abstract_indices)
    df_regex.to_csv(args.output, index=False,)
    return True

if __name__ == "__main__":
    main()