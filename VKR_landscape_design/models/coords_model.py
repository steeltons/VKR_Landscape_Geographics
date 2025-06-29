import pandas as pd

def get_coords(conn):
    return pd.read_sql('''
        SELECT coords_id, coords_coord_x, coords_coord_y, coords_territorie_id, coords_order
        FROM coords
    ''', conn)

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

def delete_coord(conn, user_coords_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM coords
        WHERE coords_id = :coordid
    ''', {"coordid": user_coords_id})
    conn.commit()

def update_coord(conn, user_coords_id, user_coord_x, user_coord_y, user_territorie_id, user_order):
    cur = conn.cursor()
    cur.execute('''
        UPDATE coords
        SET
            coords_coord_x = :usercoordx,
            coords_coord_y = :usercoordy,
            coords_territorie_id = :userterritorieid,
            coords_order = :userorder
        WHERE coords_id = :usercoordid
    ''', {
        "usercoordid": user_coords_id,
        "usercoordx": user_coord_x,
        "usercoordy": user_coord_y,
        "userterritorieid": user_territorie_id,
        "userorder": user_order
    })
    conn.commit()