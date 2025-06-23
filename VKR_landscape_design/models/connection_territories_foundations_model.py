import pandas

def get_connection_territories_foundations(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_foundations
    ''', conn)

def get_one_connection_territories_foundations(conn, user_connection_territories_foundations_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_foundations
    WHERE connection_territories_foundations_id = ''' + str(user_connection_territories_foundations_id), conn)






def find_connection_territories_foundations(conn, user_territorie_id, user_foundation_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_territories_foundations
    WHERE territorie_id = ''' + str(user_territorie_id)
                           + ' AND foundation_id = ' + str(user_foundation_id), conn)

def find_connection_territories_foundations_territorie_id(conn, user_connection_territories_foundations_id, user_territorie_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_foundations
    WHERE territorie_id = ''' + str(user_territorie_id) + ' '
    '''AND foundation_id IN 
    (SELECT foundation_id 
    FROM connection_territories_foundations
    WHERE connection_territories_foundations_id = ''' + str(user_connection_territories_foundations_id) + ')', conn)

def find_connection_territories_foundations_foundation_id(conn, user_connection_territories_foundations_id, user_foundation_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_territories_foundations
    WHERE foundation_id = ''' + str(user_foundation_id) + ' '
    '''AND territorie_id IN 
    (SELECT territorie_id 
    FROM connection_territories_foundations
    WHERE connection_territories_foundations_id = ''' + str(user_connection_territories_foundations_id) + ')', conn)





def insert_connection_territories_foundations(conn, user_territorie_id, user_foundation_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connection_territories_foundations(territorie_id, foundation_id) 
        VALUES (:userconnectionterritorieid, :userconnectionfoundationid)
        ''', {"userconnectionterritorieid": user_territorie_id, "userconnectionfoundationid": user_foundation_id})
    conn.commit()

def delete_connection_territories_foundations(conn, user_connection_territories_foundations_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connection_territories_foundations WHERE connection_territories_foundations_id = :connectionterritoriesfoundationsiddelete
        ''', {"connectionterritoriesfoundationsiddelete": user_connection_territories_foundations_id})
    conn.commit()

def update_connection_territories_foundations_territorie_id(conn, user_connection_territories_foundations_id, user_territorie_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_foundations 
        SET territorie_id = :userconnectionterritorieid 
        WHERE connection_territories_foundations_id = :userconnectionterritoriesfoundationsid
        ''', {"userconnectionterritoriesfoundationsid": user_connection_territories_foundations_id, "userconnectionterritorieid": user_territorie_id})
    conn.commit()

def update_connection_territories_foundations_foundation_id(conn, user_connection_territories_foundations_id, user_foundation_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_territories_foundations 
        SET foundation_id = :userconnectionfoundationid
        WHERE connection_territories_foundations_id = :userconnectionterritoriesfoundationsid
        ''', {"userconnectionterritoriesfoundationsid": user_connection_territories_foundations_id, "userconnectionfoundationid": user_foundation_id})
    conn.commit()
