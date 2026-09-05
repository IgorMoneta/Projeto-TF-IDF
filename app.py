import math
import re
import unicodedata

import pandas as pd
import streamlit as st


DOCUMENTOS = {
    1: "A soja requer irrigação constante durante o período de floração para garantir a produtividade.",
    2: "O controle biológico de lagartas na soja pode ser feito com a vespa Trichogramma.",
    3: "A adubação verde com leguminosas melhora o nitrogênio no solo para o milho.",
    4: "Lagartas desfolhadoras causam grande prejuízo na cultura da soja e do algodão.",
    5: "A irrigação por gotejamento economiza água e é ideal para o cultivo orgânico."
}

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das",
    "e", "em", "no", "na", "nos", "nas", "para", "por", "com", "que",
    "ser", "pode", "durante", "ao"
}


def remover_acentos(texto):
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )


def aplicar_stemmer(palavra):
    sufixos = [
        "amentos", "imentos", "adoras", "adores",
        "amento", "imento", "adora", "ador",
        "acoes", "mente", "idades", "idade",
        "icos", "icas", "oso", "osa",
        "es", "s"
    ]

    for sufixo in sufixos:
        if palavra.endswith(sufixo) and len(palavra) > len(sufixo) + 2:
            return palavra[:-len(sufixo)]

    return palavra


def preprocessar(texto, remover_stopwords=True, usar_stemming=False):
    texto = texto.lower()
    texto = remover_acentos(texto)

    tokens = re.findall(r"\b[a-z0-9]+\b", texto)

    if remover_stopwords:
        tokens = [token for token in tokens if token not in STOPWORDS]

    if usar_stemming:
        tokens = [aplicar_stemmer(token) for token in tokens]

    return tokens


def criar_indice_invertido(documentos_processados):
    indice = {}

    for doc_id, tokens in documentos_processados.items():
        for termo in set(tokens):
            if termo not in indice:
                indice[termo] = []

            indice[termo].append(doc_id)

    return dict(sorted(indice.items()))


def calcular_tf(termo, tokens_documento):
    if not tokens_documento:
        return 0

    return tokens_documento.count(termo) / len(tokens_documento)


def calcular_idf(termo, indice_invertido, total_documentos):
    documentos_com_termo = len(indice_invertido.get(termo, []))

    if documentos_com_termo == 0:
        return 0

    return math.log(total_documentos / documentos_com_termo)


def buscar(tokens_query, documentos_processados, indice_invertido):
    resultados = []
    total_documentos = len(documentos_processados)

    for doc_id, tokens_doc in documentos_processados.items():
        score_total = 0

        for termo in tokens_query:
            tf = calcular_tf(termo, tokens_doc)
            idf = calcular_idf(termo, indice_invertido, total_documentos)
            score_total += tf * idf

        if score_total > 0:
            resultados.append({
                "Documento": f"Doc {doc_id}",
                "Score TF-IDF": round(score_total, 4),
                "Texto": DOCUMENTOS[doc_id]
            })

    resultados.sort(
        key=lambda item: item["Score TF-IDF"],
        reverse=True
    )

    return resultados


st.set_page_config(
    page_title="AgroSearch",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AgroSearch")
st.write("Protótipo de motor de busca textual usando Índice Invertido e TF-IDF.")

st.sidebar.header("Configurações")

usar_stopwords = st.sidebar.checkbox(
    "Remover Stopwords",
    value=True
)

usar_stemming = st.sidebar.checkbox(
    "Aplicar Stemming",
    value=False
)

documentos_processados = {
    doc_id: preprocessar(
        texto,
        remover_stopwords=usar_stopwords,
        usar_stemming=usar_stemming
    )
    for doc_id, texto in DOCUMENTOS.items()
}

indice_invertido = criar_indice_invertido(documentos_processados)

vocabulario = sorted(indice_invertido.keys())

st.subheader("1. Documentos Processados")

df_documentos = pd.DataFrame([
    {
        "Documento": f"Doc {doc_id}",
        "Tokens": ", ".join(tokens)
    }
    for doc_id, tokens in documentos_processados.items()
])

st.dataframe(df_documentos, use_container_width=True, hide_index=True)

st.subheader("2. Vocabulário")

st.write(f"Total de termos: **{len(vocabulario)}**")
st.write(vocabulario)

st.subheader("3. Índice Invertido")

df_indice = pd.DataFrame([
    {
        "Termo": termo,
        "Documentos": ", ".join(
            f"Doc {doc_id}"
            for doc_id in docs
        )
    }
    for termo, docs in indice_invertido.items()
])

st.dataframe(df_indice, use_container_width=True, hide_index=True)

st.subheader("4. Busca")

query = st.text_input(
    "Digite uma consulta:",
    placeholder="Ex.: irrigação soja"
)

if query:
    tokens_query = preprocessar(
        query,
        remover_stopwords=usar_stopwords,
        usar_stemming=usar_stemming
    )

    st.write("Query processada:", tokens_query)

    resultados = buscar(
        tokens_query,
        documentos_processados,
        indice_invertido
    )

    if resultados:
        vencedor = resultados[0]

        st.success(
            f"Documento mais relevante: {vencedor['Documento']} "
            f"(score = {vencedor['Score TF-IDF']})"
        )

        st.write(vencedor["Texto"])

        st.subheader("Ranking")

        df_resultados = pd.DataFrame(resultados)

        st.dataframe(
            df_resultados,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("Nenhum documento relevante encontrado.")
