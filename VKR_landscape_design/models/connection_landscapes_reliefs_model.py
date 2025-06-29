import pandas as pd

def get_connections_landscapes_reliefs(conn):
    return pd.read_sql('''
        SELECT connection_id, landscape_id, relief_id
        FROM connections_landscapes_reliefs
    ''', conn)

def get_one_connection_landscapes_reliefs(conn, user_connection_id):
    return pd.read_sql(f'''
        SELECT connection_id, landscape_id, relief_id
        FROM connections_landscapes_reliefs
        WHERE connection_id = {user_connection_id}
    ''', conn)

def insert_connection_landscapes_reliefs(conn, user_landscape_id, user_relief_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connections_landscapes_reliefs(landscape_id, relief_id)
        VALUES (:userlandscapeid, :userreliefid)
    ''', {
        "userlandscapeid": user_landscape_id,
        "userreliefid": user_relief_id
    })
    conn.commit()

def delete_connection_landscapes_reliefs(conn, user_connection_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connections_landscapes_reliefs
        WHERE connection_id = :connectionid
    ''', {"connectionid": user_connection_id})
    conn.commit()

def update_connection_landscapes_reliefs(conn, user_connection_id, user_landscape_id, user_relief_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connections_landscapes_reliefs
        SET
            landscape_id = :userlandscapeid,
            relief_id = :userreliefid
        WHERE connection_id = :userconnectionid
    ''', {
        "userconnectionid": user_connection_id,
        "userlandscapeid": user_landscape_id,
        "userreliefid": user_relief_id
    })
    conn.commit()
