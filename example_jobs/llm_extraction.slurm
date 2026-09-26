#!/bin/bash
#SBATCH --job-name=g_TRUTH-test
#SBATCH --output=GT/truth_%j.out
#SBATCH --error=GT/truth_%j.err
#SBATCH --time=05:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G

set -euo pipefail

source $(conda info --base)/etc/profile.d/conda.sh
conda activate MRSA_PLN

cd ~/Staphylococcus-aureus-ResistanceAnalysis

python LLM-Extraction/llm_extration.py \
	-c-input corpora/corpus_MRSA_post_regex.csv \
        --abstract_column Abstract \
	--output extracoes/extracoes.json \
	--limite 10	

