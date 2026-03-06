from flask import Blueprint, request, jsonify
from conexion import get_connection

pagos_bp = Blueprint('pagos', _name_)

@pagos_bp.route('/', methods=['GET'])
def get_pagos():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, c.id_usuario, u.nombre AS cliente
            FROM pagos p
            JOIN compras c ON p.id_compra = c.id_compra
            JOIN usuarios u ON c.id_usuario = u.id_usuario
        """)
        pagos = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(pagos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pagos_bp.route('/<int:id>', methods=['GET'])
def get_pago(id):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pagos WHERE id_pago = %s", (id,))
        pago = cursor.fetchone()
        cursor.close()
        db.close()
        if not pago:
            return jsonify({'error': 'Pago no encontrado'}), 404
        return jsonify(pago), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pagos_bp.route('/', methods=['POST'])
def create_pago():
    data = request.get_json()
    id_compra = data.get('id_compra')
    monto = data.get('monto')
    metodo_pago = data.get('metodo_pago')
    estado = data.get('estado', 'completado')

    if not id_compra or not monto:
        return jsonify({'error': 'id_compra y monto son requeridos'}), 400

    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO pagos (id_compra, monto, metodo_pago, estado)
            VALUES (%s, %s, %s, %s)
        """, (id_compra, monto, metodo_pago, estado))
        db.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        db.close()
        return jsonify({'message': 'Pago registrado', 'id_pago': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pagos_bp.route('/compra/<int:id_compra>', methods=['GET'])
def get_pagos_compra(id_compra):
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pagos WHERE id_compra = %s", (id_compra,))
        pagos = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(pagos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500