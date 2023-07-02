from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

app = Flask(__name__)

CORS(app,resources={r"/usuarios/*":{"origins":"http://localhost"}})


conexion = MySQL(app)


@app.route('/usuarios')
def listar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, name, username,email FROM usuarios"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {'id': fila[0], 'name': fila[1], 'username': fila[2],'email': fila[3]}
            usuarios.append(usuario)
        return jsonify(usuarios)
    except Exception as ex:
        return jsonify({"message": ex})


@app.route("/usuarios/<id>")
def leer_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, name, username,email FROM usuarios WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            usuario = {'id': datos[0],'name': datos[1], 'username': datos[2],'email': datos[3]}
            return jsonify(usuario)
        else:
            return jsonify("No se encotro el usuario")
    except Exception as ex:
        return jsonify({"message": ex})


@app.route("/usuarios", methods=["POST"])
def registrar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO usuarios (name,username,email)
       VALUES ('{0}','{1}','{2}')""".format(request.json['name'],request.json['username'],request.json['email'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify("Usuario registrado")

    except Exception as ex:
        return jsonify({"message": ex})


@app.route("/usuarios/<id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM usuarios WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify("Usuario eliminado")
    except Exception as ex:
        return jsonify({"message": ex})


@app.route("/usuarios/<id>", methods=["PUT"])
def editar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = """UPDATE usuarios SET name= '{0}', username= '{1}', email= '{2}'
        WHERE id='{3}'""".format(request.json['name'], request.json['username'],request.json['email'], id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify("Usuario editado")

    except Exception as ex:
        return jsonify({"message": ex})


def pagina_no_encontrada(error):
    return jsonify({"Message":"Pagina no encontrada"}), 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
