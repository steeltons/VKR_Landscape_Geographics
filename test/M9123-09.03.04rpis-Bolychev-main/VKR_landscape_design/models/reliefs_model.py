import pandas as pd

def get_reliefs(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM reliefs 
        ORDER BY relief_name ASC
    '''

    if search_query:
        query += f'''
            WHERE relief_name LIKE '%{search_query}%'
            OR relief_description LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    reliefs = pd.read_sql(query, conn)

    if is_need_pictures:
        for index, row in reliefs.iterrows():
            picture_id = row['relief_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    reliefs.at[index, 'relief_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                reliefs.at[index, 'relief_picture_base64'] = None

    return reliefs


def get_one_relief(conn, user_relief_id, is_need_pictures=False):
    relief = pd.read_sql(f'''
        SELECT * FROM reliefs WHERE relief_id = {user_relief_id}
    ''', conn)

    if relief.empty:
        return relief

    if is_need_pictures:
        picture_id = relief.iloc[0]['relief_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                relief.at[0, 'relief_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            relief.at[0, 'relief_picture_base64'] = None

    return relief

def find_relief_name(conn, user_relief_name):
    return pd.read_sql(f'''
        SELECT relief_id
        FROM reliefs
        WHERE relief_name = "{user_relief_name}"
    ''', conn)

def find_relief_name_with_id(conn, user_relief_id, user_relief_name):
    return pd.read_sql(f'''
        SELECT relief_id
        FROM reliefs
        WHERE relief_name = "{user_relief_name}" AND relief_id != {user_relief_id}
    ''', conn)

def insert_relief(conn, user_relief_name, user_relief_description, user_relief_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO reliefs(relief_name, relief_description, relief_picture_id)
        VALUES (:userreliefname, :userreliefdescription, :userreliefpictureid)
    ''', {
        "userreliefname": user_relief_name,
        "userreliefdescription": user_relief_description,
        "userreliefpictureid": user_relief_picture_id
    })
    conn.commit()

def delete_relief(conn, user_relief_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM reliefs
        WHERE relief_id = :reliefid
    ''', {"reliefid": user_relief_id})
    conn.commit()

def update_relief(conn, user_relief_id, user_relief_name, user_relief_description, user_relief_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE reliefs
        SET
            relief_name = CASE WHEN :userreliefname IS NOT NULL THEN :userreliefname ELSE relief_name END,
            relief_description = CASE WHEN :userreliefdescription IS NOT NULL THEN :userreliefdescription ELSE relief_description END,
            relief_picture_id = CASE WHEN :userreliefpictureid IS NOT NULL THEN :userreliefpictureid ELSE relief_picture_id END
        WHERE relief_id = :userreliefid
    ''', {
        "userreliefid": user_relief_id,
        "userreliefname": user_relief_name,
        "userreliefdescription": user_relief_description,
        "userreliefpictureid": user_relief_picture_id
    })
    conn.commit()
