#!/usr/bin/python
import sqlite3



def connect_to_db():
    conn = sqlite3.connect("database.db")
    return conn


def create_db_table():
    conn = None
    try:
        conn = connect_to_db()
        conn.execute(
            """
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
            """
        )
        conn.commit()
        print("User table created successfully")
    except Exception:
        print("User table creation failed - Maybe table")
    finally:
        if conn is not None:
            conn.close()


def insert_user(user):
    inserted_user = {}
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (
                user["name"],
                user["email"],
                user["phone"],
                user["address"],
                user["country"],
            ),
        )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception:
        if conn is not None:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return inserted_user


def get_users():
    users = []
    conn = None
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["address"] = i["address"]
            user["country"] = i["country"]
            users.append(user)
    except Exception:
        users = []
    finally:
        if conn is not None:
            conn.close()
    return users


def get_user_by_id(user_id):
    user = {}
    conn = None
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"]
        user["country"] = row["country"]
    except Exception:
        user = {}
    finally:
        if conn is not None:
            conn.close()
    return user


def update_user(user):
    updated_user = {}
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
            (
                user["name"],
                user["email"],
                user["phone"],
                user["address"],
                user["country"],
                user["user_id"],
            ),
        )
        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception:
        if conn is not None:
            conn.rollback()
        updated_user = {}
    finally:
        if conn is not None:
            conn.close()
    return updated_user


def delete_user(user_id):
    message = {}
    conn = None
    try:
        conn = connect_to_db()
        conn.execute("DELETE from users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception:
        if conn is not None:
            conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        if conn is not None:
            conn.close()
    return message


if __name__ == "__main__":
    create_db_table()