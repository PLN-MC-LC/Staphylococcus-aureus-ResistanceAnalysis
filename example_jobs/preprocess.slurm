#!/bin/bash
#SBATCH --job-name=TESTES_PREPROCESS
#SBATCH --output=logs_e/testes_preprocess_%j.out
#SBATCH --error=logs_e/ERRO_testes_preprocess_%j.err
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G

set -euo pipefail

source $(conda info --base)/etc/profile.d/conda.sh
conda activate MRSA_PLN

cd ~/Staphylococcus-aureus-ResistanceAnalysis

python Preprocessing/preprocess.py \
    --input corpora/corpus_MRSA.xls \
    --output corpora/ \
    --abstract_column Abstract \
    --tokenizar \
    case-folding stop-word-removal lemmatization  
