from flask import Flask, render_template, request, redirect, url_for
from models import db, Pessoa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria o banco
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nova_pessoa = Pessoa(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            nascimento=request.form['nascimento'],
            email=request.form['email'],
            telefone=request.form['telefone'],
            matricula=request.form['matricula'],
            curso=request.form['curso'],
            sala=request.form['sala'],
            ano_ingresso=request.form['ano_ingresso'],
            cep=request.form['cep'],
            rua=request.form['rua'],
            numero=request.form['numero'],
            complemento=request.form['complemento'],
            bairro=request.form['bairro'],
            cidade=request.form['cidade'],
            estado=request.form['estado']
        )
        db.session.add(nova_pessoa)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro.html')
