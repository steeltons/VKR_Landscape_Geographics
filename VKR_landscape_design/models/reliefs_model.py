import pandas

def get_reliefs(conn):
    return pandas.read_sql('''
    SELECT relief_id, relief_name, relief_description, relief_picture  
    FROM reliefs
    ''', conn)

def find_relief_name(conn, user_relief_name):
    return pandas.read_sql('''
    SELECT * 
    FROM reliefs
    WHERE relief_name = "''' + str(user_relief_name) + '"', conn)

def get_one_relief(conn, user_relief_id):
    return pandas.read_sql('''
    SELECT relief_id, relief_name, relief_description 
    FROM reliefs 
    WHERE relief_id = ''' + str(user_relief_id), conn)

def insert_relief(conn, user_relief_name, user_relief_description):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO reliefs(relief_name, relief_description) 
        VALUES (:userreliefname, :userreliefdescription)
        ''', {"userreliefname": user_relief_name, "userreliefdescription": user_relief_description})
    conn.commit()

def delete_relief(conn, user_relief_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM reliefs WHERE relief_id = :reliefiddelete
        ''', {"reliefiddelete": user_relief_id})
    conn.commit()

def update_relief_name(conn, user_relief_id, user_relief_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE reliefs 
        SET relief_name = :userreliefname 
        WHERE relief_id = :userreliefid
        ''', {"userreliefid": user_relief_id, "userreliefname": user_relief_name})
    conn.commit()

def update_relief_description(conn, user_relief_id, user_relief_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE reliefs 
        SET relief_description = :userreliefdescription 
        WHERE relief_id = :userreliefid
        ''', {"userreliefid": user_relief_id, "userreliefdescription": user_relief_description})
    conn.commit()

def update_relief_picture(conn, user_relief_id, user_relief_picture):
    cur = conn.cursor()
    cur.execute('''
        UPDATE reliefs 
        SET relief_picture = :userreliefpicture 
        WHERE relief_id = :userreliefid
        ''', {"userreliefid": user_relief_id, "userreliefpicture": user_relief_picture})
    conn.commit()

def get_relief_picture(conn, user_relief_id):
    return pandas.read_sql('''
    SELECT relief_picture 
    FROM reliefs
    WHERE relief_id = ''' + str(user_relief_id), conn)