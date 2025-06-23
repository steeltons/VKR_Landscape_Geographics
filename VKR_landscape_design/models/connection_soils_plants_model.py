import pandas


def get_connection_soils_plants(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_soils_plants
    ''', conn)

def get_one_connection_soils_plants(conn, user_connection_soils_plants_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_soils_plants
    WHERE connection_soils_plants_id = ''' + str(user_connection_soils_plants_id), conn)






def find_connection_soils_plants(conn, user_soil_id, user_plant_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_soils_plants
    WHERE soil_id = ''' + str(user_soil_id)
                           + ' AND plant_id = ' + str(user_plant_id), conn)

def find_connection_soils_plants_soil_id(conn, user_connection_soils_plants_id, user_soil_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_soils_plants
    WHERE soil_id = ''' + str(user_soil_id) + ' '
    '''AND plant_id IN 
    (SELECT plant_id 
    FROM connection_soils_plants
    WHERE connection_soils_plants_id = ''' + str(user_connection_soils_plants_id) + ')', conn)

def find_connection_soils_plants_plant_id(conn, user_connection_soils_plants_id, user_plant_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_soils_plants
    WHERE plant_id = ''' + str(user_plant_id) + ' '
    '''AND soil_id IN 
    (SELECT soil_id 
    FROM connection_soils_plants
    WHERE connection_soils_plants_id = ''' + str(user_connection_soils_plants_id) + ')', conn)





def insert_connection_soils_plants(conn, user_soil_id, user_plant_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connection_soils_plants(soil_id, plant_id) 
        VALUES (:userconnectionsoilid, :userconnectionplantid)
        ''', {"userconnectionsoilid": user_soil_id, "userconnectionplantid": user_plant_id})
    conn.commit()

def delete_connection_soils_plants(conn, user_connection_soils_plants_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connection_soils_plants WHERE connection_soils_plants_id = :connectionsoilsplantsiddelete
        ''', {"connectionsoilsplantsiddelete": user_connection_soils_plants_id})
    conn.commit()

def update_connection_soils_plants_soil_id(conn, user_connection_soils_plants_id, user_soil_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_soils_plants 
        SET soil_id = :userconnectionsoilid 
        WHERE connection_soils_plants_id = :userconnectionsoilsplantsid
        ''', {"userconnectionsoilsplantsid": user_connection_soils_plants_id, "userconnectionsoilid": user_soil_id})
    conn.commit()

def update_connection_soils_plants_plant_id(conn, user_connection_soils_plants_id, user_plant_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_soils_plants 
        SET plant_id = :userconnectionplantid
        WHERE connection_soils_plants_id = :userconnectionsoilsplantsid
        ''', {"userconnectionsoilsplantsid": user_connection_soils_plants_id, "userconnectionplantid": user_plant_id})
    conn.commit()
