from db import get_connection

def add_transaction(user_id, t_type, category, amount, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (%s, %s, %s, %s, %s)",
                   (user_id, t_type, category, amount, date))
    conn.commit()
    cursor.close()
    conn.close()

def get_summary(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE type='income' AND user_id=%s", (user_id,))
    income = cursor.fetchone()[0]
    cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE type='expense' AND user_id=%s", (user_id,))
    expense = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"income": income, "expense": expense, "savings": income - expense}

def get_chart_data(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id=%s AND type='expense' GROUP BY category", (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data
