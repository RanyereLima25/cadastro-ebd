from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(11))
    nascimento = db.Column(db.String(10))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    matricula = db.Column(db.String(20))
    curso = db.Column(db.String(100))
    sala = db.Column(db.String(10))
    ano_ingresso = db.Column(db.String(4))
    cep = db.Column(db.String(10))
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(50))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))
