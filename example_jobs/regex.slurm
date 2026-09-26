#!/bin/bash
#SBATCH --job-name=Rgex_xtrac
#SBATCH --output=regex_1000/regex_%j.out
#SBATCH --error=regex_1000/regex_%j.err
#SBATCH --time=0:40:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=12G

set -euo pipefail

source $(conda info --base)/etc/profile.d/conda.sh
conda activate MRSA_PLN

cd ~/Staphylococcus-aureus-ResistanceAnalysis

python Regex-Extraction/regx.py \
    --input corpora/corpus_MRSA_postprocessed.csv \
    --output corpora/regex_extracted.csv \
    --abstract_column Abstract \
   
