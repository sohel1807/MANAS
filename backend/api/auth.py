import bcrypt
from database import get_connection

def register_user(name, email, password, database_url):

    conn = get_connection(database_url)
    cursor = conn.cursor()

    # Check email
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    if cursor.fetchone():
        cursor.close()
        conn.close()
        return {"message": "Email already exists"}

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        INSERT INTO users(name,email,password_hash)
        VALUES(%s,%s,%s)
        """,
        (name, email, hashed_password)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Registration Successful"}

def login_user(email, password, database_url):

    conn = get_connection(database_url)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id,password_hash
        FROM users
        WHERE email=%s
        """,
        (email,)
    )

    user = cursor.fetchone()

    if user is None:
        return {"message": "Invalid Email"}

    user_id = user[0]
    hashed_password = user[1]

    if not bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    ):
        return {"message": "Wrong Password"}

    cursor.close()
    conn.close()

    return {
        "message": "Login Successful",
        "user_id": user_id
    }