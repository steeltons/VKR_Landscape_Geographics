import pandas as pd

def get_connections_landscapes_waters(conn):
    return pd.read_sql('''
        SELECT connection_id, landscape_id, water_id
        FROM connections_landscapes_waters
    ''', conn)

def get_one_connection_landscapes_waters(conn, user_connection_id):
    return pd.read_sql(f'''
        SELECT connection_id, landscape_id, water_id
        FROM connections_landscapes_waters
        WHERE connection_id = {user_connection_id}
    ''', conn)

def insert_connection_landscapes_waters(conn, user_landscape_id, user_water_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connections_landscapes_waters(landscape_id, water_id)
        VALUES (:userlandscapeid, :userwaterid)
    ''', {
        "userlandscapeid": user_landscape_id,
        "userwaterid": user_water_id
    })
    conn.commit()

def delete_connection_landscapes_waters(conn, user_connection_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connections_landscapes_waters
        WHERE connection_id = :connectionid
    ''', {"connectionid": user_connection_id})
    conn.commit()

def update_connection_landscapes_waters(conn, user_connection_id, user_landscape_id, user_water_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connections_landscapes_waters
        SET
            landscape_id = :userlandscapeid,
            water_id = :userwaterid
        WHERE connection_id = :userconnectionid
    ''', {
        "userconnectionid": user_connection_id,
        "userlandscapeid": user_landscape_id,
        "userwaterid": user_water_id
    })
    conn.commit()
