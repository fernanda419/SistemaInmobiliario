from app.config.database import get_connection


def create_pqrs_service(data):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO pqrs (user_id, type, message, status, created_at)
    VALUES (%s,%s,%s,'pendiente',NOW())
    """

    cursor.execute(query, (
        data["user_id"],
        data["type"],
        data["message"]
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "PQRS enviada"}


def get_pqrs_service():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pqrs")

    pqrs = cursor.fetchall()

    cursor.close()
    conn.close()

    return pqrs