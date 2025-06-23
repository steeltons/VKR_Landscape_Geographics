import pandas

def get_waters(conn):
    return pandas.read_sql('''
    SELECT water_id, water_name, water_description  
    FROM waters
    ''', conn)

def find_water_name(conn, user_water_name):
    return pandas.read_sql('''
    SELECT * 
    FROM waters
    WHERE water_name = "''' + str(user_water_name) + '"', conn)

def get_one_water(conn, user_water_id):
    return pandas.read_sql('''
    SELECT water_id, water_name, water_description 
    FROM waters 
    WHERE water_id = ''' + str(user_water_id), conn)

def insert_water(conn, user_water_name, user_water_description):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO waters(water_name, water_description) 
        VALUES (:userwatername, :userwaterdescription)
        ''', {"userwatername": user_water_name, "userwaterdescription": user_water_description})
    conn.commit()

def delete_water(conn, user_water_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM waters WHERE water_id = :wateriddelete
        ''', {"wateriddelete": user_water_id})
    conn.commit()

def update_water_name(conn, user_water_id, user_water_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE waters 
        SET water_name = :userwatername 
        WHERE water_id = :userwaterid
        ''', {"userwaterid": user_water_id, "userwatername": user_water_name})
    conn.commit()

def update_water_description(conn, user_water_id, user_water_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE waters 
        SET water_description = :userwaterdescription 
        WHERE water_id = :userwaterid
        ''', {"userwaterid": user_water_id, "userwaterdescription": user_water_description})
    conn.commit()