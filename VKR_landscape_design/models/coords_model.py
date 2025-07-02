import pandas as pd

def get_coords(conn, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT coords_id, coords_coord_x, coords_coord_y, coords_territorie_id, coords_order
        FROM coords
    '''

    if search_query:
        query += f'''
            WHERE coords_coord_x LIKE '%{search_query}%'
            OR coords_coord_y LIKE '%{search_query}%'
        '''

    query += '''
        ORDER BY coords_coord_x, coords_coord_y
    '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    coords = pd.read_sql(query, conn)

    return coords

def get_one_coord(conn, user_coords_id):
    return pd.read_sql(f'''
        SELECT coords_id, coords_coord_x, coords_coord_y, coords_territorie_id, coords_order
        FROM coords
        WHERE coords_id = {user_coords_id}
    ''', conn)

def insert_coord(conn, user_coord_x, user_coord_y, user_territorie_id, user_order):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO coords(coords_coord_x, coords_coord_y, coords_territorie_id, coords_order)
        VALUES (:usercoordx, :usercoordy, :userterritorieid, :userorder)
    ''', {
        "usercoordx": user_coord_x,
        "usercoordy": user_coord_y,
        "userterritorieid": user_territorie_id,
        "userorder": user_order
    })
    conn.commit()

def update_coord(conn, user_coords_id, user_coord_x, user_coord_y, user_territorie_id, user_order):
    cur = conn.cursor()
    cur.execute('''
        UPDATE coords
        SET
            coords_coord_x = CASE WHEN :usercoordx IS NOT NULL THEN :usercoordx ELSE coords_coord_x END,
            coords_coord_y = CASE WHEN :usercoordy IS NOT NULL THEN :usercoordy ELSE coords_coord_y END,
            coords_territorie_id = CASE WHEN :userterritorieid IS NOT NULL THEN :userterritorieid ELSE coords_territorie_id END,
            coords_order = CASE WHEN :userorder IS NOT NULL THEN :userorder ELSE coords_order END
        WHERE coords_id = :usercoordid
    ''', {
        "usercoordid": user_coords_id,
        "usercoordx": user_coord_x,
        "usercoordy": user_coord_y,
        "userterritorieid": user_territorie_id,
        "userorder": user_order
    })
    conn.commit()

def delete_coord(conn, user_coords_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM coords
        WHERE coords_id = :coordid
    ''', {"coordid": user_coords_id})
    conn.commit()

