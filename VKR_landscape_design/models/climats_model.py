import pandas

def get_climats(conn):
    return pandas.read_sql('''
    SELECT climat_id, climat_name, climat_description  
    FROM climats
    ''', conn)

def find_climat_name(conn, user_climat_name):
    return pandas.read_sql('''
    SELECT * 
    FROM climats
    WHERE climat_name = "''' + str(user_climat_name) + '"', conn)

def get_one_climat(conn, user_climat_id):
    return pandas.read_sql('''
    SELECT climat_id, climat_name, climat_description 
    FROM climats 
    WHERE climat_id = ''' + str(user_climat_id), conn)

def insert_climat(conn, user_climat_name, user_climat_description):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO climats(climat_name, climat_description) 
        VALUES (:userclimatname, :userclimatdescription)
        ''', {"userclimatname": user_climat_name, "userclimatdescription": user_climat_description})
    conn.commit()

def delete_climat(conn, user_climat_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM climats WHERE climat_id = :climatiddelete
        ''', {"climatiddelete": user_climat_id})
    conn.commit()

def update_climat_name(conn, user_climat_id, user_climat_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE climats 
        SET climat_name = :userclimatname 
        WHERE climat_id = :userclimatid
        ''', {"userclimatid": user_climat_id, "userclimatname": user_climat_name})
    conn.commit()

def update_climat_description(conn, user_climat_id, user_climat_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE climats 
        SET climat_description = :userclimatdescription 
        WHERE climat_id = :userclimatid
        ''', {"userclimatid": user_climat_id, "userclimatdescription": user_climat_description})
    conn.commit()