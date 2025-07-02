import pandas as pd

def get_climats(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM climats 
        ORDER BY climat_name ASC
    '''

    if search_query:
        query += f'''
            WHERE climat_name LIKE '%{search_query}%'
            OR climat_description LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    climats = pd.read_sql(query, conn)

    if is_need_pictures:
        for index, row in climats.iterrows():
            picture_id = row['climat_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    climats.at[index, 'climat_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                climats.at[index, 'climat_picture_base64'] = None

    return climats


def get_one_climat(conn, user_climat_id, is_need_pictures=False):
    climat = pd.read_sql(f'''
        SELECT * FROM climats WHERE climat_id = {user_climat_id}
    ''', conn)

    if climat.empty:
        return climat

    if is_need_pictures:
        picture_id = climat.iloc[0]['climat_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                climat.at[0, 'climat_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            climat.at[0, 'climat_picture_base64'] = None

    return climat

def find_climat_name(conn, user_climat_name):
    return pd.read_sql(f'''
        SELECT climat_id
        FROM climats
        WHERE climat_name = "{user_climat_name}"
    ''', conn)

def find_climat_name_with_id(conn, user_climat_id, user_climat_name):
    return pd.read_sql(f'''
        SELECT climat_id
        FROM climats
        WHERE climat_name = "{user_climat_name}" AND climat_id != {user_climat_id}
    ''', conn)

def insert_climat(conn, user_climat_name, user_climat_description, user_climat_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO climats(climat_name, climat_description, climat_picture_id)
        VALUES (:userclimatname, :userclimatdescription, :userclimatpictureid)
    ''', {
        "userclimatname": user_climat_name,
        "userclimatdescription": user_climat_description,
        "userclimatpictureid": user_climat_picture_id
    })
    conn.commit()

def delete_climat(conn, user_climat_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM climats
        WHERE climat_id = :climatid
    ''', {"climatid": user_climat_id})
    conn.commit()

def update_climat(conn, user_climat_id, user_climat_name, user_climat_description, user_climat_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE climats
        SET
            climat_name = CASE WHEN :userclimatname IS NOT NULL THEN :userclimatname ELSE climat_name END,
            climat_description = CASE WHEN :userclimatdescription IS NOT NULL THEN :userclimatdescription ELSE climat_description END,
            climat_picture_id = CASE WHEN :userclimatpictureid IS NOT NULL THEN :userclimatpictureid ELSE climat_picture_id END
        WHERE climat_id = :userclimatid
    ''', {
        "userclimatid": user_climat_id,
        "userclimatname": user_climat_name,
        "userclimatdescription": user_climat_description,
        "userclimatpictureid": user_climat_picture_id
    })
    conn.commit()
