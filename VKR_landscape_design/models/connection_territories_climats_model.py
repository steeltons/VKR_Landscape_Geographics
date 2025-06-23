import pandas

def get_connection_territories_climats(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_climats
    ''', conn)

def get_one_connection_territories_climats(conn, user_connection_territories_climats_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_climats
    WHERE connection_territories_climats_id = ''' + str(user_connection_territories_climats_id), conn)






def find_connection_territories_climats(conn, user_territorie_id, user_climat_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_climats
    WHERE territorie_id = ''' + str(user_territorie_id)
                           + ' AND climat_id = ' + str(user_climat_id), conn)

def find_connection_territories_climats_territorie_id(conn, user_connection_territories_climats_id, user_territorie_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_climats
    WHERE territorie_id = ''' + str(user_territorie_id) + ' '
    '''AND climat_id IN 
    (SELECT climat_id 
    FROM connection_territories_climats
    WHERE connection_territories_climats_id = ''' + str(user_connection_territories_climats_id) + ')', conn)

def find_connection_territories_climats_climat_id(conn, user_connection_territories_climats_id, user_climat_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_climats
    WHERE climat_id = ''' + str(user_climat_id) + ' '
    '''AND territorie_id IN 
    (SELECT territorie_id 
    FROM connection_territories_climats
    WHERE connection_territories_climats_id = ''' + str(user_connection_territories_climats_id) + ')', conn)





def insert_connection_territories_climats(conn, user_territorie_id, user_climat_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connection_territories_climats(territorie_id, climat_id) 
        VALUES (:userconnectionterritorieid, :userconnectionclimatid)
        ''', {"userconnectionterritorieid": user_territorie_id, "userconnectionclimatid": user_climat_id})
    conn.commit()

def delete_connection_territories_climats(conn, user_connection_territories_climats_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connection_territories_climats WHERE connection_territories_climats_id = :connectionterritoriesclimatsiddelete
        ''', {"connectionterritoriesclimatsiddelete": user_connection_territories_climats_id})
    conn.commit()

def update_connection_territories_climats_territorie_id(conn, user_connection_territories_climats_id, user_territorie_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_climats 
        SET territorie_id = :userconnectionterritorieid 
        WHERE connection_territories_climats_id = :userconnectionterritoriesclimatsid
        ''', {"userconnectionterritoriesclimatsid": user_connection_territories_climats_id, "userconnectionterritorieid": user_territorie_id})
    conn.commit()

def update_connection_territories_climats_climat_id(conn, user_connection_territories_climats_id, user_climat_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_climats 
        SET climat_id = :userconnectionclimatid
        WHERE connection_territories_climats_id = :userconnectionterritoriesclimatsid
        ''', {"userconnectionterritoriesclimatsid": user_connection_territories_climats_id, "userconnectionclimatid": user_climat_id})
    conn.commit()