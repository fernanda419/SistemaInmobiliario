from flask import Blueprint, request, jsonify
from conexion import get_connection
import hashlib

usuarios_bp = Blueprint('usuarios', _name_)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@usuarios_bp.route('/', methods=['GET'])
def get_usuarios():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id_usuario, u.nombre, u.email, r.nombre AS rol, u.fecha_registro
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
        """)
        usuarios = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@usuarios_bp.route('/<int:id>', methods=['GET'])
def get_usuario(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id_usuario, u.nombre, u.email, r.nombre AS rol, u.fecha_registro
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """, (id,))
        usuario = cursor.fetchone()
        cursor.close()
        db.close()
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(usuario), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@usuarios_bp.route('/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    id_rol = data.get('id_rol')

    try:
        db = get_connection()
        cursor = db.cursor()
        if password:
            cursor.execute("""
                UPDATE usuarios SET nombre=%s, email=%s, password=%s, id_rol=%s
                WHERE id_usuario=%s
            """, (nombre, email, hash_password(password), id_rol, id))
        else:
            cursor.execute("""
                UPDATE usuarios SET nombre=%s, email=%s, id_rol=%s
                WHERE id_usuario=%s
            """, (nombre, email, id_rol, id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Usuario actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Usuario eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500