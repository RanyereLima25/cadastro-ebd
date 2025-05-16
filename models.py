from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    nascimento = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    matricula = db.Column(db.String(20), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    sala = db.Column(db.String(20), nullable=False)
    ano_ingresso = db.Column(db.String(4), nullable=False)
    cep = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(50))
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
