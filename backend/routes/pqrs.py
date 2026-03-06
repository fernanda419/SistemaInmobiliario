from flask import Blueprint, request, jsonify
from conexion import get_connection

pqrs_bp = Blueprint('pqrs', _name_)

@pqrs_bp.route('/', methods=['GET'])
def get_pqrs():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, u.nombre AS cliente, u.email
            FROM pqrs p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            ORDER BY p.fecha_creacion DESC
        """)
        pqrs = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(pqrs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pqrs_bp.route('/<int:id>', methods=['GET'])
def get_pqr(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, u.nombre AS cliente, u.email
            FROM pqrs p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            WHERE p.id_pqr = %s
        """, (id,))
        pqr = cursor.fetchone()
        cursor.close()
        db.close()
        if not pqr:
            return jsonify({'error': 'PQRS no encontrada'}), 404
        return jsonify(pqr), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pqrs_bp.route('/', methods=['POST'])
def create_pqr():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    tipo = data.get('tipo')  # Petición, Queja, Reclamo, Sugerencia
    asunto = data.get('asunto')
    descripcion = data.get('descripcion')

    if not id_usuario or not tipo or not descripcion:
        return jsonify({'error': 'id_usuario, tipo y descripcion son requeridos'}), 400

    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO pqrs (id_usuario, tipo, asunto, descripcion, estado)
            VALUES (%s, %s, %s, %s, 'abierto')
        """, (id_usuario, tipo, asunto, descripcion))
        db.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        db.close()
        return jsonify({'message': 'PQRS creada', 'id_pqr': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pqrs_bp.route('/<int:id>/estado', methods=['PATCH'])
def update_estado_pqr(id):
    data = request.get_json()
    estado = data.get('estado')
    respuesta = data.get('respuesta')
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE pqrs SET estado=%s, respuesta=%s WHERE id_pqr=%s
        """, (estado, respuesta, id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'PQRS actualizada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pqrs_bp.route('/usuario/<int:id_usuario>', methods=['GET'])
def get_pqrs_usuario(id_usuario):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pqrs WHERE id_usuario = %s ORDER BY fecha_creacion DESC", (id_usuario,))
        pqrs = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(pqrs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500