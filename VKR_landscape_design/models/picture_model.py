import pandas as pd

def get_pictures(conn):
    return pd.read_sql('''
        SELECT picture_id, picture_base64
        FROM pictures
    ''', conn)

def get_one_picture(conn, user_picture_id):
    return pd.read_sql(f'''
        SELECT picture_id, picture_base64
        FROM pictures
        WHERE picture_id = {user_picture_id}
    ''', conn)

def insert_picture(conn, user_picture_base64):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO pictures(picture_base64)
        VALUES (:userpicturebase64)
    ''', {
        "userpicturebase64": user_picture_base64
    })
    conn.commit()

def delete_picture(conn, user_picture_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM pictures
        WHERE picture_id = :pictureid
    ''', {"pictureid": user_picture_id})
    conn.commit()

def update_picture(conn, user_picture_id, user_picture_base64):
    cur = conn.cursor()
    cur.execute('''
        UPDATE pictures
        SET picture_base64 = :userpicturebase64
        WHERE picture_id = :userpictureid
    ''', {
        "userpictureid": user_picture_id,
        "userpicturebase64": user_picture_base64
    })
    conn.commit()
