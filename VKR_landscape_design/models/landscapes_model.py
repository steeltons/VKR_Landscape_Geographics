import pandas as pd

def get_landscapes(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM landscapes 
        ORDER BY landscape_code ASC, landscape_name ASC
    '''

    if search_query:
        query += f'''
            WHERE landscape_name LIKE '%{search_query}%'
            OR landscape_description LIKE '%{search_query}%'
            OR landscape_code LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    landscapes = pd.read_sql(query, conn)

    if is_need_pictures:
        for index, row in landscapes.iterrows():
            picture_id = row['landscape_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    landscapes.at[index, 'landscape_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                landscapes.at[index, 'landscape_picture_base64'] = None

    return landscapes


def get_one_landscape(conn, user_landscape_id, is_need_pictures=False):
    landscape = pd.read_sql(f'''
        SELECT * FROM landscapes WHERE landscape_id = {user_landscape_id}
    ''', conn)

    if landscape.empty:
        return landscape

    if is_need_pictures:
        picture_id = landscape.iloc[0]['landscape_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                landscape.at[0, 'landscape_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            landscape.at[0, 'landscape_picture_base64'] = None

    return landscape

def find_landscape_name(conn, user_landscape_name):
    return pd.read_sql(f'''
        SELECT landscape_id
        FROM landscapes
        WHERE landscape_name = "{user_landscape_name}"
    ''', conn)

def find_landscape_name_with_id(conn, user_landscape_id, user_landscape_name):
    return pd.read_sql(f'''
        SELECT landscape_id
        FROM landscapes
        WHERE landscape_name = "{user_landscape_name}" AND landscape_id != {user_landscape_id}
    ''', conn)


def insert_landscape(conn, user_landscape_name, user_landscape_code, user_landscape_description, user_landscape_area_in_square_kilometers, user_landscape_area_in_percents, user_landscape_KR, user_landscape_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO landscapes(landscape_name, landscape_code, landscape_description, landscape_area_in_square_kilometers, landscape_area_in_percents, landscape_KR, landscape_picture_id)
        VALUES (:userlandscapename, :userlandscapecode, :userlandscapedescription, :userlandscapeareainsquarekilometers, :userlandscapeareainpercents, :userlandscapekr, :userlandscapepictureid)
    ''', {
        "userlandscapename": user_landscape_name,
        "userlandscapecode": user_landscape_code,
        "userlandscapedescription": user_landscape_description,
        "userlandscapeareainsquarekilometers": user_landscape_area_in_square_kilometers,
        "userlandscapeareainpercents": user_landscape_area_in_percents,
        "userlandscapekr": user_landscape_KR,
        "userlandscapepictureid": user_landscape_picture_id
    })
    conn.commit()

def delete_landscape(conn, user_landscape_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM landscapes
        WHERE landscape_id = :landscapeid
    ''', {"landscapeid": user_landscape_id})
    conn.commit()

def update_landscape(conn, user_landscape_id, user_landscape_name, user_landscape_code, user_landscape_description, user_landscape_area_in_square_kilometers, user_landscape_area_in_percents, user_landscape_KR, user_landscape_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE landscapes
        SET
            landscape_name = CASE WHEN :userlandscapename IS NOT NULL THEN :userlandscapename ELSE landscape_name END,
            landscape_code = CASE WHEN :userlandscapecode IS NOT NULL THEN :userlandscapecode ELSE landscape_code END,
            landscape_description = CASE WHEN :userlandscapedescription IS NOT NULL THEN :userlandscapedescription ELSE landscape_description END,
            landscape_area_in_square_kilometers = CASE WHEN :userlandscapeareainsquarekilometers IS NOT NULL THEN :userlandscapeareainsquarekilometers ELSE landscape_area_in_square_kilometers END,
            landscape_area_in_percents = CASE WHEN :userlandscapeareainpercents IS NOT NULL THEN :userlandscapeareainpercents ELSE landscape_area_in_percents END,
            landscape_KR = CASE WHEN :userlandscapekr IS NOT NULL THEN :userlandscapekr ELSE landscape_KR END,
            landscape_picture_id = CASE WHEN :userlandscapepictureid IS NOT NULL THEN :userlandscapepictureid ELSE landscape_picture_id END
        WHERE landscape_id = :userlandscapeid
    ''', {
        "userlandscapeid": user_landscape_id,
        "userlandscapename": user_landscape_name,
        "userlandscapecode": user_landscape_code,
        "userlandscapedescription": user_landscape_description,
        "userlandscapeareainsquarekilometers": user_landscape_area_in_square_kilometers,
        "userlandscapeareainpercents": user_landscape_area_in_percents,
        "userlandscapekr": user_landscape_KR,
        "userlandscapepictureid": user_landscape_picture_id
    })
    conn.commit()