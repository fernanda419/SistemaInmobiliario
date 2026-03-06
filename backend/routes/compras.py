from flask import Blueprint, request, jsonify
from conexion import get_connection

compras_bp = Blueprint('compras', _name_)

@compras_bp.route('/', methods=['GET'])
def get_compras():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, u.nombre AS cliente, u.email
            FROM compras c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
        """)
        compras = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(compras), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@compras_bp.route('/<int:id>', methods=['GET'])
def get_compra(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, u.nombre AS cliente, u.email
            FROM compras c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE c.id_compra = %s
        """, (id,))
        compra = cursor.fetchone()

        if not compra:
            cursor.close()
            db.close()
            return jsonify({'error': 'Compra no encontrada'}), 404

        # Obtener los lotes de esta compra
        cursor.execute("""
            SELECT l.*
            FROM compra_lotes cl
            JOIN lotes l ON cl.id_lote = l.id_lote
            WHERE cl.id_compra = %s
        """, (id,))
        compra['lotes'] = cursor.fetchall()

        cursor.close()
        db.close()
        return jsonify(compra), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@compras_bp.route('/', methods=['POST'])
def create_compra():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    lotes_ids = data.get('lotes_ids', [])  # lista de id_lote
    monto_total = data.get('monto_total')
    estado = data.get('estado', 'pendiente')

    if not id_usuario or not lotes_ids:
        return jsonify({'error': 'id_usuario y lotes_ids son requeridos'}), 400

    try:
        db = get_connection()
        cursor = db.cursor()

        # Crear la compra
        cursor.execute("""
            INSERT INTO compras (id_usuario, monto_total, estado)
            VALUES (%s, %s, %s)
        """, (id_usuario, monto_total, estado))
        id_compra = cursor.lastrowid

        # Asociar lotes a la compra y marcarlos como vendidos
        for id_lote in lotes_ids:
            cursor.execute("""
                INSERT INTO compra_lotes (id_compra, id_lote) VALUES (%s, %s)
            """, (id_compra, id_lote))
            cursor.execute("""
                UPDATE lotes SET estado = 'vendido' WHERE id_lote = %s
            """, (id_lote,))

        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Compra registrada', 'id_compra': id_compra}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@compras_bp.route('/<int:id>/estado', methods=['PATCH'])
def update_estado_compra(id):
    data = request.get_json()
    estado = data.get('estado')
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE compras SET estado=%s WHERE id_compra=%s", (estado, id))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Estado actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@compras_bp.route('/usuario/<int:id_usuario>', methods=['GET'])
def get_compras_usuario(id_usuario):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM compras WHERE id_usuario = %s
        """, (id_usuario,))
        compras = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(compras), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500