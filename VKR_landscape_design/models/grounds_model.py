import pandas as pd

def get_grounds(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM grounds 
        ORDER BY ground_name ASC
    '''

    if search_query:
        query += f'''
            WHERE ground_name LIKE '%{search_query}%'
            OR ground_description LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    grounds = pd.read_sql(query, conn)

    if is_need_pictures:
        for index, row in grounds.iterrows():
            picture_id = row['ground_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    grounds.at[index, 'ground_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                grounds.at[index, 'ground_picture_base64'] = None

    return grounds


def get_one_ground(conn, user_ground_id, is_need_pictures=False):
    ground = pd.read_sql(f'''
        SELECT * FROM grounds WHERE ground_id = {user_ground_id}
    ''', conn)

    if ground.empty:
        return ground

    if is_need_pictures:
        picture_id = ground.iloc[0]['ground_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                ground.at[0, 'ground_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            ground.at[0, 'ground_picture_base64'] = None

    return ground

def find_ground_name(conn, user_ground_name):
    return pd.read_sql(f'''
        SELECT ground_id
        FROM grounds
        WHERE ground_name = "{user_ground_name}"
    ''', conn)

def find_ground_name_with_id(conn, user_ground_id, user_ground_name):
    return pd.read_sql(f'''
        SELECT ground_id
        FROM grounds
        WHERE ground_name = "{user_ground_name}" AND ground_id != {user_ground_id}
    ''', conn)


def insert_ground(conn, user_ground_name, user_ground_description, user_ground_density, user_ground_humidity, user_ground_solidity, user_ground_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO grounds(ground_name, ground_description, ground_density, ground_humidity, ground_solidity, ground_picture_id)
        VALUES (:usergroundname, :usergrounddescription, :usergrounddensity, :usergroundhumidity, :usergroundsolidity, :usergroundpictureid)
    ''', {
        "usergroundname": user_ground_name,
        "usergrounddescription": user_ground_description,
        "usergrounddensity": user_ground_density,
        "usergroundhumidity": user_ground_humidity,
        "usergroundsolidity": user_ground_solidity,
        "usergroundpictureid": user_ground_picture_id
    })
    conn.commit()

def delete_ground(conn, user_ground_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM grounds
        WHERE ground_id = :groundid
    ''', {"groundid": user_ground_id})
    conn.commit()

def update_ground(conn, user_ground_id, user_ground_name, user_ground_description, user_ground_density, user_ground_humidity, user_ground_solidity, user_ground_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE grounds
        SET
            ground_name = CASE WHEN :usergroundname IS NOT NULL THEN :usergroundname ELSE ground_name END,
            ground_description = CASE WHEN :usergrounddescription IS NOT NULL THEN :usergrounddescription ELSE ground_description END,
            ground_density = CASE WHEN :usergrounddensity IS NOT NULL THEN :usergrounddensity ELSE ground_density END,
            ground_humidity = CASE WHEN :usergroundhumidity IS NOT NULL THEN :usergroundhumidity ELSE ground_humidity END,
            ground_solidity = CASE WHEN :usergroundsolidity IS NOT NULL THEN :usergroundsolidity ELSE ground_solidity END,
            ground_picture_id = CASE WHEN :usergroundpictureid IS NOT NULL THEN :usergroundpictureid ELSE ground_picture_id END
        WHERE ground_id = :usergroundid
    ''', {
        "usergroundid": user_ground_id,
        "usergroundname": user_ground_name,
        "usergrounddescription": user_ground_description,
        "usergrounddensity": user_ground_density,
        "usergroundhumidity": user_ground_humidity,
        "usergroundsolidity": user_ground_solidity,
        "usergroundpictureid": user_ground_picture_id
    })
    conn.commit()