import pandas as pd

def get_foundations(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM foundations 
        ORDER BY foundation_name ASC
    '''

    if search_query:
        query += f'''
            WHERE foundation_name LIKE '%{search_query}%'
            OR foundation_description LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    foundations = pd.read_sql(query, conn)

    if is_need_pictures:
        for index, row in foundations.iterrows():
            picture_id = row['foundation_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    foundations.at[index, 'foundation_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                foundations.at[index, 'foundation_picture_base64'] = None

    return foundations


def get_one_foundation(conn, user_foundation_id, is_need_pictures=False):
    foundation = pd.read_sql(f'''
        SELECT * FROM foundations WHERE foundation_id = {user_foundation_id}
    ''', conn)

    if foundation.empty:
        return foundation

    if is_need_pictures:
        picture_id = foundation.iloc[0]['foundation_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                foundation.at[0, 'foundation_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            foundation.at[0, 'foundation_picture_base64'] = None

    return foundation

def find_foundation_name(conn, user_foundation_name):
    return pd.read_sql('''
    SELECT foundation_id 
    FROM foundations 
    WHERE foundation_name = "''' + str(user_foundation_name) + '"', conn)

def find_foundation_name_with_id(conn, user_foundation_id, user_foundation_name):
    return pd.read_sql('''
    SELECT foundation_id 
    FROM foundations 
    WHERE foundation_name = "''' + str(user_foundation_name) + '" AND foundation_id != ' + str(user_foundation_id), conn)

def insert_foundation(conn, user_foundation_name, user_foundation_description, user_foundation_depth_roof_root_in_meters, user_foundation_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO foundations(foundation_name, foundation_description, foundation_depth_roof_root_in_meters, foundation_picture_id) 
        VALUES (:userfoundationname, :userfoundationdescription, :userfoundationdepthroofrootinmeters, :userfoundationpictureid)
        ''', {"userfoundationname": user_foundation_name, "userfoundationdescription": user_foundation_description, "userfoundationdepthroofrootinmeters": user_foundation_depth_roof_root_in_meters, "userfoundationpictureid": user_foundation_picture_id})
    conn.commit()

def delete_foundation(conn, user_foundation_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM foundations WHERE foundation_id = :foundationiddelete
        ''', {"foundationiddelete": user_foundation_id})
    conn.commit()

def update_foundation(conn, user_foundation_id, user_foundation_name, user_foundation_description, user_foundation_depth_roof_root_in_meters, user_foundation_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE foundations 
        SET 
         foundation_name = CASE WHEN :userfoundationname  IS NOT NULL THEN :userfoundationname ELSE foundation_name END,  
         foundation_description = CASE WHEN :userfoundationdescription  IS NOT NULL THEN :userfoundationdescription ELSE foundation_description END,  
         foundation_depth_roof_root_in_meters = CASE WHEN :userfoundationdepthroofrootinmeters  IS NOT NULL THEN :userfoundationdepthroofrootinmeters ELSE foundation_depth_roof_root_in_meters END,  
         foundation_picture_id = CASE WHEN :userfoundationpictureid  IS NOT NULL THEN :userfoundationpictureid ELSE foundation_picture_id END 
        WHERE foundation_id = :userfoundationid 
        ''', {"userfoundationid": user_foundation_id, "userfoundationname": user_foundation_name, "userfoundationdescription": user_foundation_description, "userfoundationdepthroofrootinmeters": user_foundation_depth_roof_root_in_meters, "userfoundationpictureid": user_foundation_picture_id})
    conn.commit()

def get_foundation_picture(conn, user_foundation_id):
    return pd.read_sql('''
    SELECT foundation_picture 
    FROM foundations
    WHERE foundation_id = ''' + str(user_foundation_id), conn)