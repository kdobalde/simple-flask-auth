from flask import Flask
from models.user import User
from flask import Flask, request, jsonify
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
# view login | rota utilizada para o login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login(): # Recuperando o que o usuário enviou
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        login_user(user)
        print(current_user.is_authenticated)
        user = User.query.filter_by(username=username).first() # Retorna como uma lista

        if user and username.password == password:
                return jsonify({"message": "Autenticação realizada com sucesso"})

    return jsonify({"message": "Credenciais inválidas"}), 400

# deixar qualquer um se registrar e depois trabalhar com gerenciamento de perfil
@app.route('/user', methods=['POST'])
def create_user():
     data = request.json
     username = data.get("username")
     password = data.get("password")

     if username and password:
          user = User(username=username, password=password)
          db.session.add(user)
          db.session.commit()
          return jsonify({"message": "Usuária cadastrado com sucesso."})
     
     return jsonify({"message": "Credenciais inválidas."}), 400

@app.route('/logout', methods=['GET']) # GET pois não recebemos nada.
@login_required # rota protegida
def logout():
     logout_user()
     return jsonify({"message": "Logout realizado com sucesso!"})

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
     user = User.query.get(id_user)

     if user:
          return {"username": user.username}
     
     return jsonify({"message": "Usuário não encontrado."}), 404

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
     data = request.json
     user = User.query.get(id_user)

    # recomendado deixar mudar só a senha, pode gerar conflito, pois identificamos pelo username em rotas.
     if user and data.get("password"):
          user.password = data.get("password")
          db.session.commit()

          return jsonify({"message": f"Usuário {id_user} atualizado com sucesso."})
     
     return jsonify({"message": "Usuário não encontrado."}), 404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
     user = User.query.get(id_user)

     if id_user == current_user.id:
          return jsonify({"message": "Deleção não permitida."}), 403

     if user:
          db.session.delete(user)
          db.session.commit()
          return jsonify({"message": f"Usuário {id_user} deletado com sucesso."})
     
     return jsonify({"message": "Usuário não encontrado."}), 404


if __name__ == '__main__':
    app.run(debug=True)