import pandas

def get_connection_territories_waters(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_waters
    ''', conn)

def get_one_connection_territories_waters(conn, user_connection_territories_waters_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_waters
    WHERE connection_territories_waters_id = ''' + str(user_connection_territories_waters_id), conn)






def find_connection_territories_waters(conn, user_territorie_id, user_water_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_waters
    WHERE territorie_id = ''' + str(user_territorie_id)
                           + ' AND water_id = ' + str(user_water_id), conn)

def find_connection_territories_waters_territorie_id(conn, user_connection_territories_waters_id, user_territorie_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_waters
    WHERE territorie_id = ''' + str(user_territorie_id) + ' '
    '''AND water_id IN 
    (SELECT water_id 
    FROM connection_territories_waters
    WHERE connection_territories_waters_id = ''' + str(user_connection_territories_waters_id) + ')', conn)

def find_connection_territories_waters_water_id(conn, user_connection_territories_waters_id, user_water_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_waters
    WHERE water_id = ''' + str(user_water_id) + ' '
    '''AND territorie_id IN 
    (SELECT territorie_id 
    FROM connection_territories_waters
    WHERE connection_territories_waters_id = ''' + str(user_connection_territories_waters_id) + ')', conn)





def insert_connection_territories_waters(conn, user_territorie_id, user_water_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connection_territories_waters(territorie_id, water_id) 
        VALUES (:userconnectionterritorieid, :userconnectionwaterid)
        ''', {"userconnectionterritorieid": user_territorie_id, "userconnectionwaterid": user_water_id})
    conn.commit()

def delete_connection_territories_waters(conn, user_connection_territories_waters_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connection_territories_waters WHERE connection_territories_waters_id = :connectionterritorieswatersiddelete
        ''', {"connectionterritorieswatersiddelete": user_connection_territories_waters_id})
    conn.commit()

def update_connection_territories_waters_territorie_id(conn, user_connection_territories_waters_id, user_territorie_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_waters 
        SET territorie_id = :userconnectionterritorieid 
        WHERE connection_territories_waters_id = :userconnectionterritorieswatersid
        ''', {"userconnectionterritorieswatersid": user_connection_territories_waters_id, "userconnectionterritorieid": user_territorie_id})
    conn.commit()

def update_connection_territories_waters_water_id(conn, user_connection_territories_waters_id, user_water_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_waters 
        SET water_id = :userconnectionwaterid
        WHERE connection_territories_waters_id = :userconnectionterritorieswatersid
        ''', {"userconnectionterritorieswatersid": user_connection_territories_waters_id, "userconnectionwaterid": user_water_id})
    conn.commit()
