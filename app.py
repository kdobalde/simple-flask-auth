from flask import Flask

# Se conectando com o banco de dados
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# secret key
app.config['SECRET_KEY'] = "your_secret_key" # Proteger informações armazenadas

# onde o banco de dados vai ficar (caminho) e como vamos nos conectar | FIXO
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Conexão estabelecida

db = SQLAlchemy(app)

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)