from flask import Flask, render_template, request, redirect, url_for
from models import db, Pessoa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
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
        return redirect('/visualizar')
    return render_template('index.html')

@app.route('/visualizar')
def visualizar():
    pessoas = Pessoa.query.all()
    return render_template('visualizar.html', pessoas=pessoas)

@app.route('/excluir/<int:id>')
def excluir(id):
    pessoa = Pessoa.query.get(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect('/visualizar')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pessoa = Pessoa.query.get(id)
    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.cpf = request.form['cpf']
        pessoa.nascimento = request.form['nascimento']
        pessoa.email = request.form['email']
        pessoa.telefone = request.form['telefone']
        pessoa.matricula = request.form['matricula']
        pessoa.curso = request.form['curso']
        pessoa.sala = request.form['sala']
        pessoa.ano_ingresso = request.form['ano_ingresso']
        pessoa.cep = request.form['cep']
        pessoa.rua = request.form['rua']
        pessoa.numero = request.form['numero']
        pessoa.complemento = request.form['complemento']
        pessoa.bairro = request.form['bairro']
        pessoa.cidade = request.form['cidade']
        pessoa.estado = request.form['estado']
        db.session.commit()
        return redirect('/visualizar')
    return render_template('editar.html', pessoa=pessoa)

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

@app.route('/graficos')
def graficos():
    return render_template('graficos.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
