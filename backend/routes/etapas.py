from flask import Blueprint, request, jsonify
from conexion import get_connection

etapas_bp = Blueprint('etapas', _name_)

@etapas_bp.route('/', methods=['GET'])
def get_etapas():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etapas")
        etapas = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(etapas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@etapas_bp.route('/<int:id>', methods=['GET'])
def get_etapa(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etapas WHERE id_etapa = %s", (id,))
        etapa = cursor.fetchone()
        cursor.close()
        db.close()
        if not etapa:
            return jsonify({'error': 'Etapa no encontrada'}), 404
        return jsonify(etapa), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@etapas_bp.route('/', methods=['POST'])
def create_etapa():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    if not nombre:
        return jsonify({'error': 'El nombre es requerido'}), 400
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO etapas (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        db.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        db.close()
        return jsonify({'message': 'Etapa creada', 'id_etapa': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@etapas_bp.route('/<int:id>', methods=['PUT'])
def update_etapa(id):
    data = request.get_json()
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE etapas SET nombre=%s, descripcion=%s WHERE id_etapa=%s
        """, (data.get('nombre'), data.get('descripcion'), id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Etapa actualizada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@etapas_bp.route('/<int:id>', methods=['DELETE'])
def delete_etapa(id):
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM etapas WHERE id_etapa = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Etapa eliminada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500