import pandas

def get_connection_territories_reliefs(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_reliefs
    ''', conn)

def get_one_connection_territories_reliefs(conn, user_connection_territories_reliefs_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_reliefs
    WHERE connection_territories_reliefs_id = ''' + str(user_connection_territories_reliefs_id), conn)






def find_connection_territories_reliefs(conn, user_territorie_id, user_relief_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_reliefs
    WHERE territorie_id = ''' + str(user_territorie_id)
                           + ' AND relief_id = ' + str(user_relief_id), conn)

def find_connection_territories_reliefs_territorie_id(conn, user_connection_territories_reliefs_id, user_territorie_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_reliefs
    WHERE territorie_id = ''' + str(user_territorie_id) + ' '
    '''AND relief_id IN 
    (SELECT relief_id 
    FROM connection_territories_reliefs
    WHERE connection_territories_reliefs_id = ''' + str(user_connection_territories_reliefs_id) + ')', conn)

def find_connection_territories_reliefs_relief_id(conn, user_connection_territories_reliefs_id, user_relief_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_reliefs
    WHERE relief_id = ''' + str(user_relief_id) + ' '
    '''AND territorie_id IN 
    (SELECT territorie_id 
    FROM connection_territories_reliefs
    WHERE connection_territories_reliefs_id = ''' + str(user_connection_territories_reliefs_id) + ')', conn)





def insert_connection_territories_reliefs(conn, user_territorie_id, user_relief_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connection_territories_reliefs(territorie_id, relief_id) 
        VALUES (:userconnectionterritorieid, :userconnectionreliefid)
        ''', {"userconnectionterritorieid": user_territorie_id, "userconnectionreliefid": user_relief_id})
    conn.commit()

def delete_connection_territories_reliefs(conn, user_connection_territories_reliefs_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connection_territories_reliefs WHERE connection_territories_reliefs_id = :connectionterritoriesreliefsiddelete
        ''', {"connectionterritoriesreliefsiddelete": user_connection_territories_reliefs_id})
    conn.commit()

def update_connection_territories_reliefs_territorie_id(conn, user_connection_territories_reliefs_id, user_territorie_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_reliefs 
        SET territorie_id = :userconnectionterritorieid 
        WHERE connection_territories_reliefs_id = :userconnectionterritoriesreliefsid
        ''', {"userconnectionterritoriesreliefsid": user_connection_territories_reliefs_id, "userconnectionterritorieid": user_territorie_id})
    conn.commit()

def update_connection_territories_reliefs_relief_id(conn, user_connection_territories_reliefs_id, user_relief_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_reliefs 
        SET relief_id = :userconnectionreliefid
        WHERE connection_territories_reliefs_id = :userconnectionterritoriesreliefsid
        ''', {"userconnectionterritoriesreliefsid": user_connection_territories_reliefs_id, "userconnectionreliefid": user_relief_id})
    conn.commit()
