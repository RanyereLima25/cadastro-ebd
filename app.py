from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from collections import defaultdict
from datetime import datetime
import pytz
import os

# =============================
# CONFIGURAÇÃO DO FLASK E SUPABASE
# =============================
app = Flask(__name__)


DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://postgres:CADASTRO-EBD@db.snkyiyiojwseanmxuouo.supabase.co:5432/postgres"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "ebd-secret-key")

db = SQLAlchemy(app)

# =============================
# MODELOS
# =============================
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    ultimo_login = db.Column(db.DateTime, nullable=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(20), unique=True, nullable=False)
    nascimento = db.Column(db.Date)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(20))
    matricula = db.Column(db.String(20))
    classe = db.Column(db.String(100), nullable=False)
    sala = db.Column(db.String(20))
    ano_ingresso = db.Column(db.String(4))
    sexo = db.Column(db.String(20))
    cep = db.Column(db.String(10))
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    escolaridade = db.Column(db.String(100))
    curso_teologia = db.Column(db.String(100))
    curso_lider = db.Column(db.String(100))
    batizado = db.Column(db.String(100))
    profissao = db.Column(db.String(100))

    @staticmethod
    def gerar_matricula():
        agora = datetime.now()
        ano = agora.year
        mes = f"{agora.month:02d}"
        prefixo = f"{ano}.{mes}"
        ultimo = Pessoa.query.filter(Pessoa.matricula.like(f"{prefixo}.%")).count() + 1
        numero = f"{ultimo:04d}"
        return f"{prefixo}.{numero}"

# =============================
# DECORADORES
# =============================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# =============================
# FILTROS
# =============================
@app.template_filter('formatadata')
def formatadata(value):
    if not value:
        return "-"
    try:
        return value.strftime('%d/%m/%Y') if isinstance(value, datetime) else datetime.strptime(value, '%Y-%m-%d').strftime('%d/%m/%Y')
    except Exception:
        return value

# =============================
# ROTAS SIMPLES
# =============================
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_form = request.form['login']
        senha_form = request.form['senha']
        usuario = Usuario.query.filter_by(login=login_form).first()
        if usuario and usuario.checar_senha(senha_form):
            tz = pytz.timezone("America/Sao_Paulo")
            usuario.ultimo_login = datetime.now(tz)
            db.session.commit()
            session['usuario_id'] = usuario.id
            flash('Login realizado com sucesso.')
            return redirect(url_for('index'))
        else:
            flash('Login ou senha inválidos.')
    return render_template('login.html')

# =============================
# INICIALIZAÇÃO DO BANCO E USUARIO DE TESTE
# =============================
def init_db():
    with app.app_context():
        db.create_all()
        # Cria usuário de teste inicial se não existir
        if not Usuario.query.filter_by(login='admin').first():
            admin = Usuario(login='admin')
            admin.set_senha('123456')
            db.session.add(admin)
            db.session.commit()
            print("Usuário inicial 'admin' criado com senha '123456'.")

# =============================
# EXECUÇÃO
# =============================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)


