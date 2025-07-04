import pandas as pd

def get_connections_landscapes_soils(conn, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT connection_id, landscape_id, soil_id
        FROM connections_landscapes_soils
    '''

    if search_query:
        query += f'''
            WHERE connection_id LIKE '%{search_query}%'
            OR landscape_id LIKE '%{search_query}%'
            OR soil_id LIKE '%{search_query}%'
        '''

    query += '''
        ORDER BY landscape_id, soil_id
    '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    connections = pd.read_sql(query, conn)

    return connections


def get_one_connection_landscapes_soils(conn, user_connection_id):
    return pd.read_sql(f'''
        SELECT connection_id, landscape_id, soil_id
        FROM connections_landscapes_soils
        WHERE connection_id = {user_connection_id}
    ''', conn)

def insert_connection_landscapes_soils(conn, user_landscape_id, user_soil_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connections_landscapes_soils(landscape_id, soil_id)
        VALUES (:userlandscapeid, :usersoilid)
    ''', {
        "userlandscapeid": user_landscape_id,
        "usersoilid": user_soil_id
    })
    conn.commit()

def delete_connection_landscapes_soils(conn, user_connection_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connections_landscapes_soils
        WHERE connection_id = :connectionid
    ''', {"connectionid": user_connection_id})
    conn.commit()

def update_connection_landscapes_soils(conn, user_connection_id, user_landscape_id, user_soil_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connections_landscapes_soils
        SET
            landscape_id = :userlandscapeid,
            soil_id = :usersoilid
        WHERE connection_id = :userconnectionid
    ''', {
        "userconnectionid": user_connection_id,
        "userlandscapeid": user_landscape_id,
        "usersoilid": user_soil_id
    })
    conn.commit()
