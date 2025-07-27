from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                       (username, generate_password_hash(password)))
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()

def validate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and check_password_hash(user[1], password):
        return user[0]
    return None
