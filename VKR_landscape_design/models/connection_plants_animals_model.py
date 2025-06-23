import pandas

def get_connection_plants_animals(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_plants_animals
    ''', conn)

def get_one_connection_plants_animals(conn, user_connection_plants_animals_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_plants_animals
    WHERE connection_plants_animals_id = ''' + str(user_connection_plants_animals_id), conn)




def find_connection_plants_animals(conn, user_plant_id, user_animal_id):
    return pandas.read_sql('''
    SELECT * 
    FROM connection_plants_animals
    WHERE plant_id = ''' + str(user_plant_id)
                           + ' AND animal_id = ' + str(user_animal_id), conn)

def find_connection_plants_animals_plant_id(conn, user_connection_plants_animals_id, user_plant_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_plants_animals
    WHERE plant_id = ''' + str(user_plant_id) + ' '
    '''AND animal_id IN 
    (SELECT animal_id 
    FROM connection_plants_animals
    WHERE connection_plants_animals_id = ''' + str(user_connection_plants_animals_id) + ')', conn)

def find_connection_plants_animals_animal_id(conn, user_connection_plants_animals_id, user_animal_id):
    return pandas.read_sql('''
    SELECT *
    FROM connection_plants_animals
    WHERE animal_id = ''' + str(user_animal_id) + ' '
    '''AND plant_id IN 
    (SELECT plant_id 
    FROM connection_plants_animals
    WHERE connection_plants_animals_id = ''' + str(user_connection_plants_animals_id) + ')', conn)




def insert_connection_plants_animals(conn, user_plant_id, user_animal_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO connection_plants_animals(plant_id, animal_id) 
        VALUES (:userconnectionplantid, :userconnectionanimalid)
        ''', {"userconnectionplantid": user_plant_id, "userconnectionanimalid": user_animal_id})
    conn.commit()

def delete_connection_plants_animals(conn, user_connection_plants_animals_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM connection_plants_animals WHERE connection_plants_animals_id = :connectionplantsanimalsiddelete
        ''', {"connectionplantsanimalsiddelete": user_connection_plants_animals_id})
    conn.commit()

def update_connection_plants_animals_plant_id(conn, user_connection_plants_animals_id, user_plant_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_plants_animals 
        SET plant_id = :userconnectionplantid 
        WHERE connection_plants_animals_id = :userconnectionplantsanimalsid
        ''', {"userconnectionplantsanimalsid": user_connection_plants_animals_id, "userconnectionplantid": user_plant_id})
    conn.commit()

def update_connection_plants_animals_animal_id(conn, user_connection_plants_animals_id, user_animal_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE connection_plants_animals 
        SET animal_id = :userconnectionanimalid
        WHERE connection_plants_animals_id = :userconnectionplantsanimalsid
        ''', {"userconnectionplantsanimalsid": user_connection_plants_animals_id, "userconnectionanimalid": user_animal_id})
    conn.commit()
