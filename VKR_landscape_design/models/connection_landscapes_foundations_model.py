import pandas as pd

def get_connections_landscapes_foundations(conn):
    return pd.read_sql('''
        SELECT connection_id, landscape_id, foundation_id
        FROM connections_landscapes_foundations
    ''', conn)

def get_one_connection_landscapes_foundations(conn, user_connection_id):
    return pd.read_sql(f'''
        SELECT connection_id, landscape_id, foundation_id
        FROM connections_landscapes_foundations
        WHERE connection_id = {user_connection_id}
    ''', conn)

def insert_connection_landscapes_foundations(conn, user_landscape_id, user_foundation_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connections_landscapes_foundations(landscape_id, foundation_id)
        VALUES (:userlandscapeid, :userfoundationid)
    ''', {
        "userlandscapeid": user_landscape_id,
        "userfoundationid": user_foundation_id
    })
    conn.commit()

def delete_connection_landscapes_foundations(conn, user_connection_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connections_landscapes_foundations
        WHERE connection_id = :connectionid
    ''', {"connectionid": user_connection_id})
    conn.commit()

def update_connection_landscapes_foundations(conn, user_connection_id, user_landscape_id, user_foundation_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connections_landscapes_foundations
        SET
            landscape_id = :userlandscapeid,
            foundation_id = :userfoundationid
        WHERE connection_id = :userconnectionid
    ''', {
        "userconnectionid": user_connection_id,
        "userlandscapeid": user_landscape_id,
        "userfoundationid": user_foundation_id
    })
    conn.commit()
