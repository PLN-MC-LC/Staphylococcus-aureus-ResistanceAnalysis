SYSTEM = """
Você extrai dados de resumos de artigos científicos sobre resistência ou suscetibilidade
de Staphylococcus aureus a antibióticos.
Para cada sentença fornecida pelo usuário, extraia:
- organism: "mrsa" ou "mssa"
- property: "resistant" ou "sensitive"
- percentage: porcentagem de bactérias/isolados que apresentam a propriedade
- antibiotic: antibiótico associado à propriedade
- MDR: true ou false, indicando se a ocorrência está associada a multidrug resistance (MDR)
REGRAS:
1. Extraia apenas informações referentes a Staphylococcus aureus.
  Ignore outras espécies bacterianas.
2. Classificação de organism:
  - "MRSA": organism = "mrsa"
  - "VRSA": organism = "mrsa"
  - "MSSA": organism = "mssa"
  - "S. aureus", "Staphylococcus aureus" ou outras formas genéricas de
    Staphylococcus aureus, quando não houver indicação de MRSA ou VRSA,
    classifique organism = "mssa"
3. Se a sentença distinguir explicitamente MRSA e MSSA, mantenha os dados
  separados de acordo com o organismo correspondente.
4. Se a mesma porcentagem for explicitamente atribuída simultaneamente a
  MRSA e MSSA, classifique organism = "mssa", EXCETO quando a informação
  também estiver associada a MDR. Nesse caso, aplique a regra 9.
5. Se a bactéria for associada explicitamente a "multidrug resistance",
  "multidrug-resistant", "MDR" ou expressão equivalente, classifique
  MDR = true.
6. Se não houver evidência de MDR para aquela ocorrência, classifique
  MDR = false.
7. Quando a sentença afirmar que 100% dos isolados/bactérias apresentam
  a propriedade, mas não fornecer uma porcentagem explícita, use
  percentage = 100.
8. Não invente porcentagens. Se a sentença não fornecer uma porcentagem
  explícita nem permitir concluir que corresponde a 100%, não extraia
  essa ocorrência.
9. Se MRSA e MSSA forem indistinguíveis quanto à porcentagem e a informação
  estiver associada a MDR, registre DUAS ocorrências:
  - uma com organism = "mrsa" e MDR = true
  - uma com organism = "mssa" e MDR = true
10. A propriedade deve ser classificada exclusivamente como:
   - "resistant" para resistência
   - "sensitive" para suscetibilidade
11. Resistência e suscetibilidade devem ser armazenadas como ocorrências
   separadas. Nunca transforme uma propriedade na outra por inferência.
12. Se uma bactéria tiver sido tratada simultaneamente com mais de um
   antibiótico e a propriedade observada for "sensitive", ignore essa
   ocorrência.
13. Quando uma mesma propriedade e porcentagem forem explicitamente
   associadas a vários antibióticos, registre uma ocorrência para cada
   antibiótico.
14. Não associe uma porcentagem a um antibiótico se a sentença não deixar
   clara essa associação.
15. Se não houver nenhuma informação que satisfaça as regras acima,
   responda exatamente:
   {"extracoes":[]}
FORMATO DE SAÍDA:
Responda APENAS com JSON válido, sem cercas de markdown e sem qualquer
texto adicional.
O JSON deve seguir exatamente este formato:
{
 "extracoes": [
   {
     "organism": "mrsa" ou "mssa",
     "property": "resistant" ou "sensitive",
     "percentage": número,
     "antibiotic": "nome do antibiótico",
     "MDR": true ou false
   }
 ]
}
"""
abstract = """
from 1 january to 31 december 2014, 27 institutions around australia participated in the australian staphylococcal sepsis outcome programme (assop). the aim of assop 2014 was to determine the proportion of staphylococcus aureus bacteraemia (sab) isolates in australia that are antimicrobial resistant, with particular emphasis on susceptibility to methicillin and to characterise the molecular epidemiology of the isolates. overall, 18.8% of the 2,206 sab episodes were methicillin resistant, which was significantly higher than that reported in most european countries. the 30-day all-cause mortality associated with methicillin-resistant sab was 23.4%, which was significantly higher than the 14.4% mortality associated with methicillin-sensitive sab (p<0.0001). with the exception of the beta-lactams and erythromycin, antimicrobial resistance in methicillin-sensitive s. aureus remains rare. however in addition to the beta-lactams, approximately 50% of methicillin-resistant s. aureus (mrsa) were resistant to erythromycin and ciprofloxacin and approximately 15% were resistant to co-trimoxazole, tetracycline and gentamicin. when applying the european committee on antimicrobial susceptibility testing breakpoints, teicoplanin resistance was detected in 2 s. aureus isolates. resistance was not detected for vancomycin or linezolid. resistance to non-beta-lactam anti-microbials was largely attributable to 2 healthcare-associated mrsa clones; st22-iv [2b] (emrsa-15) and st239-iii [3a] (aus-2/3 emrsa). st22-iv [2b] (emrsa-15) has become the predominant healthcare associated clone in australia. sixty per cent of methicillin-resistant sab were due to community-associated (ca) clones. although polyclonal, almost 44% of community-associated clones were characterised as st93-iv [2b] (queensland ca-mrsa) and st1-iv [2b] (wa1). ca-mrsa, in particular the st45-v [5c2&5] (wa84) clone, has acquired multiple antimicrobial resistance determinants including ciprofloxacin, erythromycin, clindamycin, gentamicin and tetracycline. as ca-mrsa is well established in the australian community it is important that antimicrobial resistance patterns in community and healthcare-associated sab is monitored as this information will guide therapeutic practices in treating s. aureus sepsis.
"""

json = """
{
"extracoes": [
  {
   "organism": "MRSA",
   "value": "50%",
   "property": "resistant",
   "MDR": True,
   "antibiotic": "erythromycin"
  },
  {
   "organism": "MRSA",
   "value": "50%",
   "property": "resistant",
   "MDR": True,
   "antibiotic": "ciprofloxacin"
  },
  {
   "organism": "MRSA",
   "value": "15%",
   "property": "resistant",
   "MDR": True,
   "antibiotic": "co-trimoxazole"
  },
  {
   "organism": "MRSA",
   "value": "15%",
   "property": "resistant",
   "MDR": True,
   "antibiotic": "tetracycline"
  },
  {
   "organism": "MRSA",
   "value": "15%",
   "property": "resistant",
   "MDR": True,
   "antibiotic": "gentamicina"
  }
]
}
"""


ASSISTANT = [(abstract, json)]
