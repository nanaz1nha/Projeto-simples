from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'seu_usuario'  # Substitua pelo seu usuário MySQL
app.config['MYSQL_PASSWORD'] = 'sua_senha'  # Substitua pela sua senha MySQL
app.config['MYSQL_DB'] = 'cliente_db'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['POST'])
def add_cliente():
    nome = request.form['nome']
    telefone = request.form['telefone']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO clientes (nome, telefone) VALUES (%s, %s)", (nome, telefone))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('index'))

@app.route('/clientes', methods=['GET'])
def get_clientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    return jsonify(clientes)

@app.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({'message': 'Cliente deletado'}), 200

if __name__ == '__main__':
    app.run(debug=True)
