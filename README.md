# 🧬 Staphylococcus aureus - Resistance Analysis
> Extração e análise de informações sobre resistência antimicrobiana em *Staphylococcus aureus* (MRSA) a partir de textos científicos, combinando Processamento de Linguagem Natural clássico (Regex, SciSpaCy) e Modelos de Linguagem (LLMs).

<!------------------------------------>

## 🔎 Sumário

- [Sumário](#🔎-sumário)
- [Descrição](#-descrição)
- [Estrutura do repositório](#-estrutura-do-repositório)
- [Como rodar?](#-como-rodar)
- [Professores](#-professores-responsáveis)
- [Colaboradores](#-colaboradores)
- [Licença](#-licença)

<!------------------------------------>

## 📝 Descrição

#### ❓O que é MRSA?

*Staphylococcus aureus* é uma bactéria que faz parte da microbiota humana, mas que pode causar desde infecções leves de pele até quadros graves, como pneumonia e sepse. Quando a cepa é resistente à meticilina e a outros antibióticos β-lactâmicos, ela é chamada de **MRSA** (*Methicillin-Resistant Staphylococcus aureus*), considerada um dos principais patógenos de infecções hospitalares e um problema crescente de saúde pública.

#### ⁉️Qual o problema?

A literatura científica sobre resistência em *S. aureus* é enorme e cresce todos os dias. As informações importantes (antibióticos testados, genes de resistência, perfis de sensibilidade, cepas, etc.) estão espalhadas em texto livre, o que torna inviável reunir tudo na mão.

#### ❗O que o nosso projeto faz?

Este projeto, desenvolvido na disciplina de Processamento de Linguagem Natural, constrói um pipeline que:

1. Pré-processa os textos científicos (limpeza, tokenização, remoção de _stopwords_, etc.);
2. Extrai com LLM após refinamento do _dataset_ usando REGEX.
3. Plota gráficos com base nas extrações.

## 📂 Estrutura do repositório

| Pasta / Arquivo | Descrição |
|---|---|
| `Preprocessing/` | Etapa de pré-processamento dos textos |
| `Regex-Extraction/` | Extração de informações com expressões regulares |
| `LLM-Extraction/` | Extração de informações com LLMs |
| `LLM-Analysis/` | Análise dos resultados obtidos pelos LLMs |
| `extracoes/` | Saídas das extrações |
| `metadata/` | Search query usada para obtenção dos arquivos |
| `plots/` | Gráficos gerados na análise |
| `example_jobs/` | Exemplos de *jobs* para execução do pipeline |
| `environment.yml` | Definição do ambiente Conda (`MRSA_PLN`) |
| `setup.sh` | Script que cria o ambiente e instala os modelos necessários |
| `.env.example` | Modelo do arquivo de variáveis de ambiente |

## 👨‍💻 Como rodar?

### 📋 Pré-requisitos

1. Ter o [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda ou Anaconda) instalado.
2. Um sistema com `bash` (Linux, macOS ou WSL no Windows).
3. Uma chave de API para acessar os LLMs (necessária apenas para as etapas de `LLM-Extraction` e `LLM-Analysis`).

### ⚙️ Configurando o ambiente

1. Clone o repositório:

```bash
git clone https://github.com/PLN-MC-LC/Staphylococcus-aureus-ResistanceAnalysis.git
cd Staphylococcus-aureus-ResistanceAnalysis
```

2. Execute o script de instalação:

```bash
bash setup.sh
```

3. Ative o ambiente:

```bash
conda activate MRSA_PLN
```

### 🔑 Configurando a chave de API

Copie o arquivo de exemplo e preencha com a sua chave:

```bash
cp .env.example .env
```

## 👨‍🏫 Professores responsáveis

> O trabalho realizado não seria possível sem a ajuda do professor Dr. James de Almeida da disciplina Processamento de Linguagem Natural e Imagens

<div align="center">
  <table>
    <tr>
        <td align="center">
        <a href="#" title="Prof. James M. de Almeida">
            <img src="https://avatars.githubusercontent.com/u/108157661?v=4" width="100px;" alt="Foto do James do Github"/><br>
            <a href="https://github.com/jamesmalmeida"><b>Prof. Dr. James M. de Almeida<b></a>
        </a>
        </td>
    </tr>
  </table>
</div>

<!--
## ⭐ Agradecimentos

> BlindText

-->
## 🤝 Colaboradores

<div align="center">
  <table>
    <tr>
      <td align="center" width="150">
        <a href="https://github.com/LucasCandinho" title="Lucas Candinho">
          <img src="https://avatars.githubusercontent.com/u/149116352?v=4" width="100" height="100" style="object-fit: cover;" alt="Foto do Lucas do Github"/><br>
          <b>Lucas Candinho</b>
        </a>
      </td>
      <td align="center" width="150">
        <a href="https://github.com/mncunha" title="Matheus N. Cunha">
          <img src="https://avatars.githubusercontent.com/u/209475678?v=4" width="100" height="100" style="object-fit: cover;" alt="Foto do Matheus do Github"/><br>
          <b>Matheus N. Cunha</b>
        </a>
      </td>
    </tr>
  </table>
</div>

<!---
### 💪 Como cada colaborador contribuiu?

> Lucas Candinho: Lorem Ipsum

> Matheus N. Cunha: Lorem Ipsum

--->

## 📄 Licença

Este projeto está licenciado sob a [GNU General Public License v3.0](LICENSE).

![alt text](https://ilum.cnpem.br/wp-content/uploads/2026/07/ilum-defeso-2026-1536x188.png "Logo da Ilum completa")

<!------------------------------------>