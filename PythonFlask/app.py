from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'\xd7\x04\xf5\x85\n\x03\xe7\xe6{u\xf5\x01\x02;\xd7\x90'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'

db = SQLAlchemy(app)

frutas = []
registros = []


class cursos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(50))
	descricao = db.Column(db.String(100))
	ch = db.Column(db.Integer)

	def __init__(self, nome, descricao, ch):
		self.nome = nome
		self.descricao = descricao
		self.ch = ch


@app.route('/', methods=["GET", "POST"])
def principal():
	#frutas = ["Morango", "Uva", "Laranja", "Mamão", "Macã", "Pera", "Melão", "Abacaxi"]
	if request.method == "POST":
		if request.form.get("fruta"):
			frutas.append(request.form.get("fruta"))
	return render_template("index.html", frutas=frutas)

@app.route('/sobre', methods=["GET", "POST"])
def sobre():
	#notas = {"Fulano":5.0, "Beltrano":6.0, "Aluno":7.0, "Sicrano":8.5, "Rodrigo":9.5}
	if request.method == "POST":
		if request.form.get("aluno") and request.form.get("nota"):
			registros.append({"aluno": request.form.get("aluno"), "nota": request.form.get("nota")})
	return render_template("sobre.html", registros=registros)

@app.route('/filmes/<propriedade>')
def filmes(propriedade):
	if propriedade == 'populares':
		url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=758b036ebdeae222d06885d1e3fb555a"
	elif propriedade == 'kids':
		url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=758b036ebdeae222d06885d1e3fb555a"
	elif propriedade == '2010':
		url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=758b036ebdeae222d06885d1e3fb555a"
	elif propriedade == 'drama':
		url = "https://api.themoviedb.org/3/discover/movie?with_genres=18&primary_release_year=2014&api_key=758b036ebdeae222d06885d1e3fb555a"
	elif propriedade == 'tom_cruise':
		url = "https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=758b036ebdeae222d06885d1e3fb555a"
	
	resposta = urllib.request.urlopen(url)

	dados = resposta.read()
	
	jsondata = json.loads(dados)

	return render_template("filmes.html", filmes=jsondata['results'])


@app.route('/cursos')
def lista_cursos():
	page = request.args.get('page', 1, type=int)
	per_page = 4
	todos_cursos = cursos.query.paginate(page=page, per_page=per_page)
	return render_template("cursos.html", cursos=todos_cursos)


@app.route('/cria_curso', methods=["GET", "POST"])
def cria_curso():
	nome = request.form.get('nome')
	descricao = request.form.get('descricao')
	ch = request.form.get('ch')

	if request.method == 'POST':
		if not nome or not descricao or not ch:
			flash("Preencha todos os campos do formulário", "error")	
		else:
			curso = cursos(nome, descricao, ch)
			db.session.add(curso)
			db.session.commit()
			return redirect(url_for('lista_cursos'))
	return render_template("novo_curso.html")


@app.route('/<int:id>/atualiza_curso', methods=["GET", "POST"])
def atualiza_curso(id):
	curso = cursos.query.filter_by(id=id).first()
	if request.method == 'POST':
		nome = request.form["nome"]
		descricao = request.form["descricao"]
		ch = request.form["ch"]

		cursos.query.filter_by(id=id).update({"nome":nome, "descricao":descricao, "ch":ch})
		db.session.commit()
		return redirect(url_for('lista_cursos'))
	return render_template("atualiza_curso.html", curso=curso)


@app.route('/<int:id>/remove_curso')
def remove_curso(id):
	curso = cursos.query.filter_by(id=id).first()
	db.session.delete(curso)
	db.session.commit()
	return redirect(url_for('lista_cursos'))


if __name__ =="__main__":
	with app.app_context():
		db.create_all()
		app.run(debug=True)