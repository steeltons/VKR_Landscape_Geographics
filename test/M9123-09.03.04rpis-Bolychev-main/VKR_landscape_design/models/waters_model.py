import pandas as pd

def get_waters(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM waters 
        ORDER BY water_name ASC
    '''

    if search_query:
        query += f'''
            WHERE water_name LIKE '%{search_query}%'
            OR water_description LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    waters = pd.read_sql(query, conn)

    if is_need_pictures:
        for index, row in waters.iterrows():
            picture_id = row['water_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    waters.at[index, 'water_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                waters.at[index, 'water_picture_base64'] = None

    return waters


def get_one_water(conn, user_water_id, is_need_pictures=False):
    water = pd.read_sql(f'''
        SELECT * FROM waters WHERE water_id = {user_water_id}
    ''', conn)

    if water.empty:
        return water

    if is_need_pictures:
        picture_id = water.iloc[0]['water_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                water.at[0, 'water_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            water.at[0, 'water_picture_base64'] = None

    return water

def find_water_name(conn, user_water_name):
    return pd.read_sql(f'''
        SELECT water_id
        FROM waters
        WHERE water_name = "{user_water_name}"
    ''', conn)

def find_water_name_with_id(conn, user_water_id, user_water_name):
    return pd.read_sql(f'''
        SELECT water_id
        FROM waters
        WHERE water_name = "{user_water_name}" AND water_id != {user_water_id}
    ''', conn)

def insert_water(conn, user_water_name, user_water_description, user_water_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO waters(water_name, water_description, water_picture_id)
        VALUES (:userwatername, :userwaterdescription, :userwaterpictureid)
    ''', {
        "userwatername": user_water_name,
        "userwaterdescription": user_water_description,
        "userwaterpictureid": user_water_picture_id
    })
    conn.commit()

def delete_water(conn, user_water_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM waters
        WHERE water_id = :waterid
    ''', {"waterid": user_water_id})
    conn.commit()

def update_water(conn, user_water_id, user_water_name, user_water_description, user_water_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE waters
        SET
            water_name = CASE WHEN :userwatername IS NOT NULL THEN :userwatername ELSE water_name END,
            water_description = CASE WHEN :userwaterdescription IS NOT NULL THEN :userwaterdescription ELSE water_description END,
            water_picture_id = CASE WHEN :userwaterpictureid IS NOT NULL THEN :userwaterpictureid ELSE water_picture_id END
        WHERE water_id = :userwaterid
    ''', {
        "userwaterid": user_water_id,
        "userwatername": user_water_name,
        "userwaterdescription": user_water_description,
        "userwaterpictureid": user_water_picture_id
    })
    conn.commit()