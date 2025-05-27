import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Consulta EBD", page_icon="📖", layout="wide")

st.title("📖 Consulta de Alunos - EBD")

# Conectando ao banco de dados
engine = create_engine('sqlite:///cadastro.db')

# Consulta SQL
query = """
SELECT 
    id,
    nome,
    cpf,
    nascimento,
    email,
    telefone,
    tipo,
    matricula,
    classe,
    sala,
    ano_ingresso,
    cep,
    rua,
    numero,
    complemento,
    bairro,
    cidade,
    estado
FROM pessoa
"""

# Carrega dados
df = pd.read_sql(query, engine)

# Exibir a tabela
st.subheader("Lista de Alunos Cadastrados")
st.dataframe(df, use_container_width=True)

# Filtros simples
classe = st.selectbox("Filtrar por Classe", ["Todas"] + sorted(df['classe'].dropna().unique().tolist()))
if classe != "Todas":
    df = df[df['classe'] == classe]

st.dataframe(df, use_container_width=True)
