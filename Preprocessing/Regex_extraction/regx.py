import regex as re
import pandas as pd
import spacy
from utils_proprocess import (importar_arq)

nlp = spacy.load('en_core_sci_sm')



i = -1

for abstract in df["Abstract"]:
    i+=1
    doc = nlp(str(abstract))
    for sentence in doc.sents:
        property = re.search(r"\b(?:susceptible|sensitive)\b", str(sentence), re.IGNORECASE)

        if property!=None:
            value = re.search(
                r"\d+(?:\.\d+)?\s*%",
                str(sentence)
            )

            if value!=None:
                antibiotic = re.search(
                    r"\b(?:to|against)\s+([A-Za-z]+(?:[- ][A-Za-z]+)*)",
                    str(sentence),
                    re.IGNORECASE
                )

                if antibiotic != None:

                    print(
                        'No Abstract', i,
                        'MRSA é', property[0],
                        'a', antibiotic.group(1),
                        'em', value[0]
                    )

                    print(
                        'Sentença de extração do abstract',
                        i, ':', sentence
                    )