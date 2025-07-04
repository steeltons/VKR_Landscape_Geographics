import pandas as pd

def get_soils(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM soils 
        ORDER BY soil_name ASC
    '''

    if search_query:
        query += f'''
            WHERE soil_name LIKE '%{search_query}%'
            OR soil_description LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    soils = pd.read_sql(query, conn)

    if is_need_pictures:
        for index, row in soils.iterrows():
            picture_id = row['soil_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    soils.at[index, 'soil_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                soils.at[index, 'soil_picture_base64'] = None

    return soils


def get_one_soil(conn, user_soil_id, is_need_pictures=False):
    soil = pd.read_sql(f'''
        SELECT * FROM soils WHERE soil_id = {user_soil_id}
    ''', conn)

    if soil.empty:
        return soil

    if is_need_pictures:
        picture_id = soil.iloc[0]['soil_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                soil.at[0, 'soil_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            soil.at[0, 'soil_picture_base64'] = None

    return soil

def find_soil_name(conn, user_soil_name):
    return pd.read_sql(f'''
        SELECT soil_id
        FROM soils
        WHERE soil_name = "{user_soil_name}"
    ''', conn)

def find_soil_name_with_id(conn, user_soil_id, user_soil_name):
    return pd.read_sql(f'''
        SELECT soil_id
        FROM soils
        WHERE soil_name = "{user_soil_name}" AND soil_id != {user_soil_id}
    ''', conn)

def insert_soil(conn, user_soil_name, user_soil_description, user_soil_acidity, user_soil_minerals, user_soil_profile, user_soil_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO soils(soil_name, soil_description, soil_acidity, soil_minerals, soil_profile, soil_picture_id)
        VALUES (:usersoilname, :usersoildescription, :usersoilacidity, :usersoilminerals, :usersoilprofile, :usersoilpictureid)
    ''', {
        "usersoilname": user_soil_name,
        "usersoildescription": user_soil_description,
        "usersoilacidity": user_soil_acidity,
        "usersoilminerals": user_soil_minerals,
        "usersoilprofile": user_soil_profile,
        "usersoilpictureid": user_soil_picture_id
    })
    conn.commit()

def delete_soil(conn, user_soil_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM soils
        WHERE soil_id = :soilid
    ''', {"soilid": user_soil_id})
    conn.commit()

def update_soil(conn, user_soil_id, user_soil_name, user_soil_description, user_soil_acidity, user_soil_minerals, user_soil_profile, user_soil_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE soils
        SET
            soil_name = CASE WHEN :usersoilname IS NOT NULL THEN :usersoilname ELSE soil_name END,
            soil_description = CASE WHEN :usersoildescription IS NOT NULL THEN :usersoildescription ELSE soil_description END,
            soil_acidity = CASE WHEN :usersoilacidity IS NOT NULL THEN :usersoilacidity ELSE soil_acidity END,
            soil_minerals = CASE WHEN :usersoilminerals IS NOT NULL THEN :usersoilminerals ELSE soil_minerals END,
            soil_profile = CASE WHEN :usersoilprofile IS NOT NULL THEN :usersoilprofile ELSE soil_profile END,
            soil_picture_id = CASE WHEN :usersoilpictureid IS NOT NULL THEN :usersoilpictureid ELSE soil_picture_id END
        WHERE soil_id = :usersoilid
    ''', {
        "usersoilid": user_soil_id,
        "usersoilname": user_soil_name,
        "usersoildescription": user_soil_description,
        "usersoilacidity": user_soil_acidity,
        "usersoilminerals": user_soil_minerals,
        "usersoilprofile": user_soil_profile,
        "usersoilpictureid": user_soil_picture_id
    })
    conn.commit()
