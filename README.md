# 🌱 AgroSearch

O **AgroSearch** é um protótipo de motor de busca textual desenvolvido em Python com Streamlit.

A aplicação recebe uma consulta do usuário, processa o texto e retorna os documentos mais relevantes utilizando **Índice Invertido** e **TF-IDF**, implementados manualmente.

O projeto tem foco em demonstrar, de forma simples e visual, conceitos fundamentais de recuperação de informação e processamento de texto.

---

## 🚀 Funcionalidades

- Normalização de textos
- Conversão para letras minúsculas
- Remoção de acentos
- Tokenização
- Remoção opcional de Stopwords
- Stemming opcional
- Geração dinâmica de vocabulário
- Construção de Índice Invertido
- Cálculo manual de TF
- Cálculo manual de IDF
- Cálculo manual de TF-IDF
- Ranqueamento de documentos por relevância
- Destaque do documento mais relevante
- Interface interativa com Streamlit

---

## 🧠 Como funciona

O fluxo principal do AgroSearch é:

```text
Documentos
    ↓
Pré-processamento
    ↓
Tokenização
    ↓
Normalização
    ↓
Stopwords / Stemming
    ↓
Índice Invertido
    ↓
Consulta do usuário
    ↓
Pré-processamento da consulta
    ↓
TF + IDF
    ↓
TF-IDF
    ↓
Ranking dos documentos
```

---

## 🔎 Índice Invertido

O índice invertido relaciona cada termo aos documentos em que ele aparece.

Exemplo:

```python
{
    "soja": [1, 2, 4],
    "irrigacao": [1, 5],
    "milho": [3]
}
```

Isso permite identificar rapidamente quais documentos possuem determinado termo.

---

## 📊 TF-IDF

O AgroSearch utiliza TF-IDF para calcular a relevância dos documentos.

### TF — Term Frequency

Mede a frequência de um termo dentro de um documento.

```text
TF(t,d) = frequência do termo / quantidade total de termos do documento
```

### IDF — Inverse Document Frequency

Mede o quanto um termo é raro entre os documentos.

```text
IDF(t) = log(N / DF(t))
```

Onde:

- `N` = quantidade total de documentos
- `DF(t)` = quantidade de documentos que possuem o termo

### TF-IDF

```text
TF-IDF(t,d) = TF(t,d) × IDF(t)
```

Quando uma consulta possui mais de uma palavra, os valores de TF-IDF são somados para gerar o score final de cada documento.

---

## 🖥️ Interface

A aplicação possui uma interface simples utilizando Streamlit.

O usuário pode:

- ativar ou desativar Stopwords;
- ativar ou desativar Stemming;
- visualizar os documentos processados;
- visualizar o vocabulário;
- visualizar o Índice Invertido;
- realizar buscas;
- visualizar o ranking dos documentos.

---

## 📚 Base de documentos

A versão atual utiliza uma pequena base de textos relacionados à agricultura.

Exemplos de temas:

- soja;
- irrigação;
- controle biológico;
- lagartas;
- milho;
- algodão;
- cultivo orgânico.

A base pode ser facilmente substituída ou expandida.

---

## 🔍 Exemplos de busca

Algumas consultas que podem ser utilizadas:

```text
soja
```

```text
irrigação
```

```text
lagartas
```

```text
milho
```

```text
irrigação soja
```

O sistema calcula a relevância de cada documento e apresenta os resultados do maior para o menor score.

---

## 🛠️ Tecnologias

- Python
- Streamlit
- Pandas
- Regex (`re`)
- Unicodedata
- Math

O cálculo de TF-IDF e a construção do Índice Invertido foram implementados manualmente, sem uso de `TfidfVectorizer` ou soluções equivalentes.

---

## 📁 Estrutura

```text
AgroSearch/
│
├── app.py
└── README.md
```

---

## ▶️ Como executar

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/AgroSearch.git
```

Entre na pasta:

```bash
cd AgroSearch
```

Instale as dependências:

```bash
pip install streamlit pandas
```

Execute a aplicação:

```bash
streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador.

---

## 🧩 Principais funções

| Função | Responsabilidade |
|---|---|
| `remover_acentos()` | Remove acentos dos textos |
| `aplicar_stemmer()` | Aplica stemming simplificado |
| `preprocessar()` | Executa o pipeline de processamento |
| `criar_indice_invertido()` | Cria a relação termo-documento |
| `calcular_tf()` | Calcula a frequência do termo |
| `calcular_idf()` | Calcula a raridade do termo |
| `buscar()` | Calcula os scores e gera o ranking |

---

## 💡 Possíveis evoluções

Algumas melhorias que podem ser adicionadas futuramente:

- Similaridade de Cosseno
- BM25
- Importação de documentos externos
- Suporte a arquivos PDF
- Persistência do índice
- Busca em uma base maior de documentos
- Destaque dos termos encontrados
- Comparação entre diferentes métodos de ranqueamento
- API para integração com outros sistemas

---

## 📌 Objetivo do projeto

O AgroSearch demonstra como um mecanismo de busca textual pode ser construído a partir de conceitos básicos de recuperação de informação.

Em vez de depender de ferramentas prontas para realizar todo o processo, o projeto implementa as principais etapas de forma explícita, tornando possível visualizar o funcionamento interno de:

```text
Texto → Tokens → Índice → TF-IDF → Ranking
```

Isso torna o projeto útil tanto para experimentação quanto para evolução futura em sistemas de busca e processamento de linguagem natural.
