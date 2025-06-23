import pandas

def get_foundations(conn):
    return pandas.read_sql('''
    SELECT foundation_id, foundation_name, foundation_description, foundation_picture  
    FROM foundations
    ''', conn)

def find_foundation_name(conn, user_foundation_name):
    return pandas.read_sql('''
    SELECT * 
    FROM foundations
    WHERE foundation_name = "''' + str(user_foundation_name) + '"', conn)

def get_one_foundation(conn, user_foundation_id):
    return pandas.read_sql('''
    SELECT foundation_id, foundation_name, foundation_description 
    FROM foundations 
    WHERE foundation_id = ''' + str(user_foundation_id), conn)

def insert_foundation(conn, user_foundation_name, user_foundation_description):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO foundations(foundation_name, foundation_description) 
        VALUES (:userfoundationname, :userfoundationdescription)
        ''', {"userfoundationname": user_foundation_name, "userfoundationdescription": user_foundation_description})
    conn.commit()

def delete_foundation(conn, user_foundation_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM foundations WHERE foundation_id = :foundationiddelete
        ''', {"foundationiddelete": user_foundation_id})
    conn.commit()

def update_foundation_name(conn, user_foundation_id, user_foundation_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE foundations 
        SET foundation_name = :userfoundationname 
        WHERE foundation_id = :userfoundationid
        ''', {"userfoundationid": user_foundation_id, "userfoundationname": user_foundation_name})
    conn.commit()

def update_foundation_description(conn, user_foundation_id, user_foundation_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE foundations 
        SET foundation_description = :userfoundationdescription 
        WHERE foundation_id = :userfoundationid
        ''', {"userfoundationid": user_foundation_id, "userfoundationdescription": user_foundation_description})
    conn.commit()

def update_foundation_picture(conn, user_foundation_id, user_foundation_picture):
    cur = conn.cursor()
    cur.execute('''
        UPDATE foundations 
        SET foundation_picture = :userfoundationpicture 
        WHERE foundation_id = :userfoundationid
        ''', {"userfoundationid": user_foundation_id, "userfoundationpicture": user_foundation_picture})
    conn.commit()

def get_foundation_picture(conn, user_foundation_id):
    return pandas.read_sql('''
    SELECT foundation_picture 
    FROM foundations
    WHERE foundation_id = ''' + str(user_foundation_id), conn)