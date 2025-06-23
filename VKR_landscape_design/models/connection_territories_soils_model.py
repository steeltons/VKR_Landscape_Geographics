import pandas

def get_connection_territories_soils(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_soils
    ''', conn)

def get_one_connection_territories_soils(conn, user_connection_territories_soils_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_soils
    WHERE connection_territories_soils_id = ''' + str(user_connection_territories_soils_id), conn)






def find_connection_territories_soils(conn, user_territorie_id, user_soil_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_soils
    WHERE territorie_id = ''' + str(user_territorie_id)
                           + ' AND soil_id = ' + str(user_soil_id), conn)

def find_connection_territories_soils_territorie_id(conn, user_connection_territories_soils_id, user_territorie_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_soils
    WHERE territorie_id = ''' + str(user_territorie_id) + ' '
    '''AND soil_id IN 
    (SELECT soil_id 
    FROM connection_territories_soils
    WHERE connection_territories_soils_id = ''' + str(user_connection_territories_soils_id) + ')', conn)

def find_connection_territories_soils_soil_id(conn, user_connection_territories_soils_id, user_soil_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_soils
    WHERE soil_id = ''' + str(user_soil_id) + ' '
    '''AND territorie_id IN 
    (SELECT territorie_id 
    FROM connection_territories_soils
    WHERE connection_territories_soils_id = ''' + str(user_connection_territories_soils_id) + ')', conn)





def insert_connection_territories_soils(conn, user_territorie_id, user_soil_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connection_territories_soils(territorie_id, soil_id) 
        VALUES (:userconnectionterritorieid, :userconnectionsoilid)
        ''', {"userconnectionterritorieid": user_territorie_id, "userconnectionsoilid": user_soil_id})
    conn.commit()

def delete_connection_territories_soils(conn, user_connection_territories_soils_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connection_territories_soils WHERE connection_territories_soils_id = :connectionterritoriessoilsiddelete
        ''', {"connectionterritoriessoilsiddelete": user_connection_territories_soils_id})
    conn.commit()

def update_connection_territories_soils_territorie_id(conn, user_connection_territories_soils_id, user_territorie_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_soils 
        SET territorie_id = :userconnectionterritorieid 
        WHERE connection_territories_soils_id = :userconnectionterritoriessoilsid
        ''', {"userconnectionterritoriessoilsid": user_connection_territories_soils_id, "userconnectionterritorieid": user_territorie_id})
    conn.commit()

def update_connection_territories_soils_soil_id(conn, user_connection_territories_soils_id, user_soil_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_soils 
        SET soil_id = :userconnectionsoilid
        WHERE connection_territories_soils_id = :userconnectionterritoriessoilsid
        ''', {"userconnectionterritoriessoilsid": user_connection_territories_soils_id, "userconnectionsoilid": user_soil_id})
    conn.commit()