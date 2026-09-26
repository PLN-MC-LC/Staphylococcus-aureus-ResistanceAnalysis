#!/usr/bin/env bash

set -e

ENV_NAME="MRSA_PLN"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cria as pastas necessárias
mkdir -p "$ROOT/extracoes"
mkdir -p "$ROOT/corpora"

source $(conda info --base)/etc/profile.d/conda.sh


eval "$(conda shell.bash hook)"

if conda env list | grep -q "^${ENV_NAME} "; then
    conda env update -n "$ENV_NAME" -f "$ROOT/environment.yml" --prune
else
    conda env create -f "$ROOT/environment.yml"
fi

conda activate "$ENV_NAME"

python -m nltk.downloader stopwords

python -m pip install \
    https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz

python -m pip install \
    https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_md-0.5.4.tar.gz

python -m pip install \
    https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_scibert-0.5.4.tar.gz

echo
echo "==> Testando instalação..."

python - <<'PY'
import spacy
import scispacy

print("spaCy:", spacy.__version__)
print("SciSpaCy:", scispacy.__version__)

for model in [
    "en_core_sci_sm",
    "en_core_sci_md",
    "en_core_sci_scibert",
]:
    nlp = spacy.load(model)
    print(f"OK: {model}")

print("Tudo funcionando!")
PY

echo
echo "======================================"
echo " Ambiente configurado com sucesso!"
echo "======================================"
echo
echo "Para ativá-lo:"
echo "conda activate ${ENV_NAME}"
