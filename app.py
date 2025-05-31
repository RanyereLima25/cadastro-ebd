import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import plotly.express as px

# ----- Configuração do banco -----
engine = create_engine('sqlite:///cadastro.db')
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# ----- Modelos -----
class Pessoa(Base):
    __tablename__ = 'pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    nascimento = Column(String)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    tipo = Column(String)
    matricula = Column(String)
    classe = Column(String, nullable=False)
    sala = Column(String)
    ano_ingresso = Column(String)
    cep = Column(String)
    rua = Column(String)
    numero = Column(String)
    complemento = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

Base.metadata.create_all(engine)

# ----- Funções -----
def autenticar(login, senha):
    usuario = db.query(Usuario).filter(Usuario.login == login).first()
    if usuario and usuario.checar_senha(senha):
        return True
    return False

def listar_pessoas(busca=''):
    if busca:
        return db.query(Pessoa).filter(Pessoa.nome.ilike(f'%{busca}%')).all()
    return db.query(Pessoa).all()

def adicionar_pessoa(**kwargs):
    nova = Pessoa(**kwargs)
    db.add(nova)
    db.commit()

def excluir_pessoa(pessoa_id):
    pessoa = db.query(Pessoa).get(pessoa_id)
    db.delete(pessoa)
    db.commit()

# ----- Interface -----
st.set_page_config(page_title="Sistema de Cadastro", layout="wide")
st.title("Sistema de Cadastro e Relatórios")

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# ---- LOGIN ----
if not st.session_state.autenticado:
    st.subheader("Login")
    login = st.text_input("Usuário")
    senha = st.text_input("Senha", type='password')
    if st.button("Entrar"):
        if autenticar(login, senha):
            st.session_state.autenticado = True
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha inválidos.")
    st.stop()

# ---- MENU ----
menu = st.sidebar.selectbox(
    "Menu",
    ["Cadastro de Pessoa", "Visualizar Dados", "Relatórios", "Gráficos", "Sair"]
)

if menu == "Sair":
    st.session_state.autenticado = False
    st.experimental_rerun()

# ---- CADASTRO ----
if menu == "Cadastro de Pessoa":
    st.subheader("Cadastrar Pessoa")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        nascimento = st.date_input("Nascimento")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        tipo = st.selectbox("Tipo", ["Aluno", "Professor", "Outro"])
        matricula = st.text_input("Matrícula")
        classe = st.text_input("Classe")
        sala = st.text_input("Sala")
        ano_ingresso = st.text_input("Ano de ingresso")
        cep = st.text_input("CEP")
        rua = st.text_input("Rua")
        numero = st.text_input("Número")
        complemento = st.text_input("Complemento")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")

        enviar = st.form_submit_button("Salvar")

        if enviar:
            adicionar_pessoa(
                nome=nome, cpf=cpf, nascimento=str(nascimento),
                email=email, telefone=telefone, tipo=tipo,
                matricula=matricula, classe=classe, sala=sala,
                ano_ingresso=ano_ingresso, cep=cep, rua=rua,
                numero=numero, complemento=complemento, bairro=bairro,
                cidade=cidade, estado=estado
            )
            st.success("Pessoa cadastrada com sucesso!")

# ---- VISUALIZAR ----
elif menu == "Visualizar Dados":
    st.subheader("Lista de Pessoas")
    busca = st.text_input("Buscar pelo nome")
    pessoas = listar_pessoas(busca)

    df = pd.DataFrame([vars(p) for p in pessoas])
    if not df.empty:
        df = df.drop(columns=['_sa_instance_state'])
        st.dataframe(df)
    else:
        st.info("Nenhum registro encontrado.")

    if st.checkbox("Excluir Pessoa"):
        id_excluir = st.number_input("ID da Pessoa para excluir", min_value=1)
        if st.button("Excluir"):
            excluir_pessoa(id_excluir)
            st.success("Pessoa excluída com sucesso.")

# ---- RELATÓRIOS ----
elif menu == "Relatórios":
    st.subheader("Relatório por Classe")
    dados = db.query(Pessoa.classe, func.count(Pessoa.id)).group_by(Pessoa.classe).all()
    df = pd.DataFrame(dados, columns=['Classe', 'Quantidade'])
    st.table(df)

# ---- GRÁFICOS ----
elif menu == "Gráficos":
    st.subheader("Gráfico por Classe")
    dados = db.query(Pessoa.classe, func.count(Pessoa.id)).group_by(Pessoa.classe).all()
    df = pd.DataFrame(dados, columns=['Classe', 'Quantidade'])

    fig = px.bar(df, x='Classe', y='Quantidade', title="Quantidade por Classe")
    st.plotly_chart(fig)
