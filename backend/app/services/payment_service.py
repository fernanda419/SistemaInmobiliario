from app.config.database import get_connection


def create_payment_service(payment):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO payments (purchase_id, amount, payment_date)
    VALUES (%s,%s,NOW())
    """

    cursor.execute(query, (
        payment["purchase_id"],
        payment["amount"]
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Pago registrado"}


def get_payments_service():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM payments")

    payments = cursor.fetchall()

    cursor.close()
    conn.close()

    return payments