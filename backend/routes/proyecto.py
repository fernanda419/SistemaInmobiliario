from flask import Blueprint, request, jsonify
from conexion import get_connection

proyecto_bp = Blueprint('proyecto', _name_)

@proyecto_bp.route('/', methods=['GET'])
def get_proyecto():
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM proyecto_info LIMIT 1")
        proyecto = cursor.fetchone()
        cursor.close()
        db.close()
        if not proyecto:
            return jsonify({'error': 'No hay información del proyecto'}), 404
        return jsonify(proyecto), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@proyecto_bp.route('/', methods=['PUT'])
def update_proyecto():
    data = request.get_json()
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM proyecto_info")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""
                INSERT INTO proyecto_info (nombre, descripcion, ubicacion, imagen_url)
                VALUES (%s, %s, %s, %s)
            """, (data.get('nombre'), data.get('descripcion'), data.get('ubicacion'), data.get('imagen_url')))
        else:
            cursor.execute("""
                UPDATE proyecto_info SET nombre=%s, descripcion=%s, ubicacion=%s, imagen_url=%s
                LIMIT 1
            """, (data.get('nombre'), data.get('descripcion'), data.get('ubicacion'), data.get('imagen_url')))

        db.commit()
        cursor.close()
        db.close()
        return jsonify({'message': 'Información del proyecto actualizada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500