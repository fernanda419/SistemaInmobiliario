from flask import Blueprint, request, jsonify
from conexion import get_connection

lotes_bp = Blueprint('lotes', _name_)

@lotes_bp.route('/', methods=['GET'])
def get_lotes():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*, e.nombre AS etapa_nombre
            FROM lotes l
            LEFT JOIN etapas e ON l.id_etapa = e.id_etapa
        """)
        lotes = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(lotes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lotes_bp.route('/<int:id>', methods=['GET'])
def get_lote(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*, e.nombre AS etapa_nombre
            FROM lotes l
            LEFT JOIN etapas e ON l.id_etapa = e.id_etapa
            WHERE l.id_lote = %s
        """, (id,))
        lote = cursor.fetchone()
        cursor.close()
        db.close()
        if not lote:
            return jsonify({'error': 'Lote no encontrado'}), 404
        return jsonify(lote), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lotes_bp.route('/', methods=['POST'])
def create_lote():
    data = request.get_json()
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO lotes (area, precio, estado, id_etapa)
            VALUES (%s, %s, %s, %s)
        """, (data.get('area'), data.get('precio'), data.get('estado', 'disponible'), data.get('id_etapa')))
        db.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        db.close()
        return jsonify({'message': 'Lote creado', 'id_lote': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lotes_bp.route('/<int:id>', methods=['PUT'])
def update_lote(id):
    data = request.get_json()
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE lotes SET area=%s, precio=%s, estado=%s, id_etapa=%s
            WHERE id_lote=%s
        """, (data.get('area'), data.get('precio'), data.get('estado'), data.get('id_etapa'), id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Lote actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lotes_bp.route('/<int:id>', methods=['DELETE'])
def delete_lote(id):
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM lotes WHERE id_lote = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Lote eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lotes_bp.route('/disponibles', methods=['GET'])
def get_lotes_disponibles():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.*, e.nombre AS etapa_nombre
            FROM lotes l
            LEFT JOIN etapas e ON l.id_etapa = e.id_etapa
            WHERE l.estado = 'disponible'
        """)
        lotes = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(lotes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500