from flask import Blueprint, request, jsonify
from conexion import get_connection
import hashlib

auth_bp = Blueprint('auth', _name_)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email y contraseña requeridos'}), 400

    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id_usuario, u.nombre, u.email, r.nombre AS rol
            FROM usuarios u
            JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.email = %s AND u.password = %s
        """, (email, hash_password(password)))
        usuario = cursor.fetchone()
        cursor.close()
        db.close()

        if usuario:
            return jsonify({'message': 'Login exitoso', 'usuario': usuario}), 200
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    id_rol = data.get('id_rol', 2)  # Default: Cliente

    if not nombre or not email or not password:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password, id_rol)
            VALUES (%s, %s, %s, %s)
        """, (nombre, email, hash_password(password), id_rol))
        db.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        db.close()
        return jsonify({'message': 'Usuario registrado exitosamente', 'id_usuario': nuevo_id}), 201
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'El email ya está registrado'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500