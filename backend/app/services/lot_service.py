from app.config.database import get_connection


def get_all_lots():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM lots")

    lots = cursor.fetchall()

    cursor.close()
    conn.close()

    return lots


def add_lot(lot):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO lots (area, location, price, stage, status)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (
        lot["area"],
        lot["location"],
        lot["price"],
        lot["stage"],
        lot["status"]
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Lote creado"}