import pandas as pd

def get_pictures(conn, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT picture_id, picture_base64
        FROM pictures
    '''

    if search_query:
        query += f'''
            WHERE picture_id LIKE '%{search_query}%'
        '''

    query += '''
        ORDER BY picture_id
    '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    pictures = pd.read_sql(query, conn)

    return pictures


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
