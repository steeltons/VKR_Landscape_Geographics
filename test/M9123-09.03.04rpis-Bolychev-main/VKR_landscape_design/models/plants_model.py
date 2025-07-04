import pandas as pd

def get_plants(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM plants 
        ORDER BY plant_name ASC
    '''

    if search_query:
        query += f'''
            WHERE plant_name LIKE '%{search_query}%'
            OR plant_description LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    plants = pd.read_sql(query, conn)

    if is_need_pictures:
        for index, row in plants.iterrows():
            picture_id = row['plant_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    plants.at[index, 'plant_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                plants.at[index, 'plant_picture_base64'] = None

    return plants


def get_one_plant(conn, user_plant_id, is_need_pictures=False):
    plant = pd.read_sql(f'''
        SELECT * FROM plants WHERE plant_id = {user_plant_id}
    ''', conn)

    if plant.empty:
        return plant

    if is_need_pictures:
        picture_id = plant.iloc[0]['plant_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                plant.at[0, 'plant_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            plant.at[0, 'plant_picture_base64'] = None

    return plant

def find_plant_name(conn, user_plant_name):
    return pd.read_sql(f'''
        SELECT plant_id
        FROM plants
        WHERE plant_name = "{user_plant_name}"
    ''', conn)

def find_plant_name_with_id(conn, user_plant_id, user_plant_name):
    return pd.read_sql(f'''
        SELECT plant_id
        FROM plants
        WHERE plant_name = "{user_plant_name}" AND plant_id != {user_plant_id}
    ''', conn)

def insert_plant(conn, user_plant_name, user_plant_description, user_plant_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO plants(plant_name, plant_description, plant_picture_id)
        VALUES (:userplantname, :userplantdescription, :userplantpictureid)
    ''', {
        "userplantname": user_plant_name,
        "userplantdescription": user_plant_description,
        "userplantpictureid": user_plant_picture_id
    })
    conn.commit()

def delete_plant(conn, user_plant_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM plants
        WHERE plant_id = :plantid
    ''', {"plantid": user_plant_id})
    conn.commit()

def update_plant(conn, user_plant_id, user_plant_name, user_plant_description, user_plant_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants
        SET
            plant_name = CASE WHEN :userplantname IS NOT NULL THEN :userplantname ELSE plant_name END,
            plant_description = CASE WHEN :userplantdescription IS NOT NULL THEN :userplantdescription ELSE plant_description END,
            plant_picture_id = CASE WHEN :userplantpictureid IS NOT NULL THEN :userplantpictureid ELSE plant_picture_id END
        WHERE plant_id = :userplantid
    ''', {
        "userplantid": user_plant_id,
        "userplantname": user_plant_name,
        "userplantdescription": user_plant_description,
        "userplantpictureid": user_plant_picture_id
    })
    conn.commit()
