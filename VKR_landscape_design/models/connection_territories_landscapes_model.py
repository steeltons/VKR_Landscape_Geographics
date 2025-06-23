import pandas

def get_connection_territories_landscapes(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_landscapes
    ''', conn)

def get_one_connection_territories_landscapes(conn, user_connection_territories_landscapes_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_landscapes
    WHERE connection_territories_landscapes_id = ''' + str(user_connection_territories_landscapes_id), conn)






def find_connection_territories_landscapes(conn, user_territorie_id, user_landscape_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_landscapes
    WHERE territorie_id = ''' + str(user_territorie_id)
                           + ' AND landscape_id = ' + str(user_landscape_id), conn)

def find_connection_territories_landscapes_territorie_id(conn, user_connection_territories_landscapes_id, user_territorie_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_landscapes
    WHERE territorie_id = ''' + str(user_territorie_id) + ' '
    '''AND landscape_id IN 
    (SELECT landscape_id 
    FROM connection_territories_landscapes
    WHERE connection_territories_landscapes_id = ''' + str(user_connection_territories_landscapes_id) + ')', conn)

def find_connection_territories_landscapes_landscape_id(conn, user_connection_territories_landscapes_id, user_landscape_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_landscapes
    WHERE landscape_id = ''' + str(user_landscape_id) + ' '
    '''AND territorie_id IN 
    (SELECT territorie_id 
    FROM connection_territories_landscapes
    WHERE connection_territories_landscapes_id = ''' + str(user_connection_territories_landscapes_id) + ')', conn)





def insert_connection_territories_landscapes(conn, user_territorie_id, user_landscape_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connection_territories_landscapes(territorie_id, landscape_id) 
        VALUES (:userconnectionterritorieid, :userconnectionlandscapeid)
        ''', {"userconnectionterritorieid": user_territorie_id, "userconnectionlandscapeid": user_landscape_id})
    conn.commit()

def delete_connection_territories_landscapes(conn, user_connection_territories_landscapes_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connection_territories_landscapes WHERE connection_territories_landscapes_id = :connectionterritorieslandscapesiddelete
        ''', {"connectionterritorieslandscapesiddelete": user_connection_territories_landscapes_id})
    conn.commit()

def update_connection_territories_landscapes_territorie_id(conn, user_connection_territories_landscapes_id, user_territorie_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_landscapes 
        SET territorie_id = :userconnectionterritorieid 
        WHERE connection_territories_landscapes_id = :userconnectionterritorieslandscapesid
        ''', {"userconnectionterritorieslandscapesid": user_connection_territories_landscapes_id, "userconnectionterritorieid": user_territorie_id})
    conn.commit()

def update_connection_territories_landscapes_landscape_id(conn, user_connection_territories_landscapes_id, user_landscape_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_landscapes 
        SET landscape_id = :userconnectionlandscapeid
        WHERE connection_territories_landscapes_id = :userconnectionterritorieslandscapesid
        ''', {"userconnectionterritorieslandscapesid": user_connection_territories_landscapes_id, "userconnectionlandscapeid": user_landscape_id})
    conn.commit()
