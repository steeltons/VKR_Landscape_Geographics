import pandas

def get_landscapes(conn):
    return pandas.read_sql('''
    SELECT landscape_id, landscape_name, landscape_description, landscape_picture  
    FROM landscapes
    ''', conn)

def find_landscape_name(conn, user_landscape_name):
    return pandas.read_sql('''
    SELECT * 
    FROM landscapes
    WHERE landscape_name = "''' + str(user_landscape_name) + '"', conn)

def get_one_landscape(conn, user_landscape_id):
    return pandas.read_sql('''
    SELECT landscape_id, landscape_name, landscape_description 
    FROM landscapes 
    WHERE landscape_id = ''' + str(user_landscape_id), conn)

def insert_landscape(conn, user_landscape_name, user_landscape_description):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO landscapes(landscape_name, landscape_description) 
        VALUES (:userlandscapename, :userlandscapedescription)
        ''', {"userlandscapename": user_landscape_name, "userlandscapedescription": user_landscape_description})
    conn.commit()

def delete_landscape(conn, user_landscape_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM landscapes WHERE landscape_id = :landscapeiddelete
        ''', {"landscapeiddelete": user_landscape_id})
    conn.commit()

def update_landscape_name(conn, user_landscape_id, user_landscape_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE landscapes 
        SET landscape_name = :userlandscapename 
        WHERE landscape_id = :userlandscapeid
        ''', {"userlandscapeid": user_landscape_id, "userlandscapename": user_landscape_name})
    conn.commit()

def update_landscape_description(conn, user_landscape_id, user_landscape_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE landscapes 
        SET landscape_description = :userlandscapedescription 
        WHERE landscape_id = :userlandscapeid
        ''', {"userlandscapeid": user_landscape_id, "userlandscapedescription": user_landscape_description})
    conn.commit()

def update_landscape_picture(conn, user_landscape_id, user_landscape_picture):
    cur = conn.cursor()
    cur.execute('''
        UPDATE landscapes 
        SET landscape_picture = :userlandscapepicture 
        WHERE landscape_id = :userlandscapeid
        ''', {"userlandscapeid": user_landscape_id, "userlandscapepicture": user_landscape_picture})
    conn.commit()

def get_landscape_picture(conn, user_landscape_id):
    return pandas.read_sql('''
    SELECT landscape_picture 
    FROM landscapes
    WHERE landscape_id = ''' + str(user_landscape_id), conn)