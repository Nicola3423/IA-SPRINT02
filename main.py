import streamlit as st
import pandas as pd
from Oracledb import carregar_dados_pacientes, carregar_dados_sintoma

# Carregar dados do banco de dados
data = carregar_dados_pacientes()
data2 = carregar_dados_sintoma()

# Normalizar nomes das colunas para evitar erros
data2.columns = data2.columns.str.lower().str.strip()


# Verificar se a coluna correta existe antes de acessá-la
if 'sintoma_descricao' in data2.columns:
    sintomas_unicos = data2['sintoma_descricao'].dropna().unique()
else:
    st.error("A coluna 'sintoma_descricao' não foi encontrada no DataFrame.")
    sintomas_unicos = []

# Interface do Streamlit
title = "Dashboard de Predição - Pacientes Odontológicos"
st.title(title)
st.write("Visualização dos Dados:")
st.dataframe(data)

# Seção de inserção de dados para predição
st.header("Inserir Dados para Predição")
data_consulta = st.text_input("Data da consulta")

# Seleção do Sintoma
Sintoma = st.selectbox("Sintoma", options=sintomas_unicos)

# Seletor de Gravidade
gravidade = st.slider("Gravidade do Sintoma (1-3)", min_value=1, max_value=3, value=2)

# Função para classificar risco
def classificar_risco(gravidade):
    if gravidade == 1:
        return "Baixo"
    elif gravidade == 2:
        return "Médio"
    else:
        return "Alto"

# Calcular risco do paciente
risco = classificar_risco(gravidade)
st.write(f"🔍 **Risco Calculado:** {risco}")

# Dicionário de recomendações para sintomas
recomendacoes = {
    "Dor de cabeça": "Tomar analgésico leve e repousar.",
    "Febre alta": "Consultar um médico e manter hidratação.",
    "Náuseas": "Evitar alimentos gordurosos e manter hidratação.",
    "Cansaço extremo": "Descansar e verificar exames médicos.",
    "Tontura": "Monitorar pressão arterial e procurar auxílio médico se necessário."
}

# Exibir recomendação baseada no sintoma
tratamento = recomendacoes.get(Sintoma, "Nenhuma recomendação específica encontrada.")
st.write(f"💡 **Recomendação:** {tratamento}")

# Alerta para casos de alto risco
if risco == "Alto":
    st.error("🚨 ALTA PRIORIDADE: O paciente precisa de atenção urgente!")