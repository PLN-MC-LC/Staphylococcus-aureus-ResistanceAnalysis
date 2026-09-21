import regex as re
import pandas as pd
import spacy
from utils_preprocess import (importar_arq)
from utils_regex import get_regex, verifica_regex


amostra = verifica_regex(
    properties,
    antibiotics,
    values,
    sentence,
    abstract_indices,
    5
)

for (
    property_,
    antibiotic,
    value,
    sentence,
    abstract_index
) in amostra:

    print("Abstract:", abstract_index)
    print("MRSA:", property_)
    print("Antibiótico:", antibiotic)
    print("Valor:", value)
    print("Sentença:", sentence)
    print("-" * 80)