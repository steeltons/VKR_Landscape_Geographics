import pandas

def get_grounds(conn):
    return pandas.read_sql('''
    SELECT ground_id, ground_name, ground_description, ground_density, ground_humidity, ground_hardness_Moos, ground_picture 
    FROM grounds
    ''', conn)

def get_one_ground(conn, user_ground_id):
    return pandas.read_sql('''
    SELECT ground_id, ground_name, ground_description, ground_density, ground_humidity, ground_hardness_Moos 
    FROM grounds 
    WHERE ground_id = ''' + str(user_ground_id), conn)

def find_ground_name(conn, user_ground_name):
    return pandas.read_sql('''
    SELECT * 
    FROM grounds
    WHERE ground_name = "''' + str(user_ground_name) + '"', conn)

def insert_ground(conn, user_ground_name, user_ground_description):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO grounds(ground_name, ground_description) 
        VALUES (:usergroundname, :usergrounddescription)
        ''', {"usergroundname": user_ground_name, "usergrounddescription": user_ground_description})
    conn.commit()

def delete_ground(conn, user_ground_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM grounds WHERE ground_id = :groundiddelete
        ''', {"groundiddelete": user_ground_id})
    conn.commit()

def update_ground_name(conn, user_ground_id, user_ground_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE grounds 
        SET ground_name = :usergroundname 
        WHERE ground_id = :usergroundid
        ''', {"usergroundid": user_ground_id, "usergroundname": user_ground_name})
    conn.commit()

def update_ground_description(conn, user_ground_id, user_ground_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE grounds 
        SET ground_description = :usergrounddescription 
        WHERE ground_id = :usergroundid
        ''', {"usergroundid": user_ground_id, "usergrounddescription": user_ground_description})
    conn.commit()

def update_ground_density(conn, user_ground_id, user_ground_density):
    cur = conn.cursor()
    cur.execute('''
        UPDATE grounds 
        SET ground_density = :usergrounddensity 
        WHERE ground_id = :usergroundid
        ''', {"usergroundid": user_ground_id, "usergrounddensity": user_ground_density})
    conn.commit()

def update_ground_humidity(conn, user_ground_id, user_ground_humidity):
    cur = conn.cursor()
    cur.execute('''
        UPDATE grounds 
        SET ground_humidity = :usergroundhumidity 
        WHERE ground_id = :usergroundid
        ''', {"usergroundid": user_ground_id, "usergroundhumidity": user_ground_humidity})
    conn.commit()

def update_ground_hardness_Moos(conn, user_ground_id, user_ground_hardness_Moos):
    cur = conn.cursor()
    cur.execute('''
        UPDATE grounds 
        SET ground_hardness_Moos = :usergroundhardness_Moos 
        WHERE ground_id = :usergroundid
        ''', {"usergroundid": user_ground_id, "usergroundhardness_Moos": user_ground_hardness_Moos})
    conn.commit()

def update_ground_picture(conn, user_ground_id, user_ground_picture):
    cur = conn.cursor()
    cur.execute('''
        UPDATE grounds 
        SET ground_picture = :usergroundpicture 
        WHERE ground_id = :usergroundid
        ''', {"usergroundid": user_ground_id, "usergroundpicture": user_ground_picture})
    conn.commit()

def get_ground_picture(conn, user_ground_id):
    return pandas.read_sql('''
    SELECT ground_picture 
    FROM grounds
    WHERE ground_id = ''' + str(user_ground_id), conn)