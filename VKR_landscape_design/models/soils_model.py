import pandas

def get_soils(conn):
    return pandas.read_sql('''
    SELECT soil_id, soil_name, soil_description, soil_acidity, soil_minerals, soil_profile, soil_picture 
    FROM soils
    ''', conn)

def get_one_soil(conn, user_soil_id):
    return pandas.read_sql('''
    SELECT soil_id, soil_name, soil_description, soil_acidity, soil_minerals, soil_profile 
    FROM soils 
    WHERE soil_id = ''' + str(user_soil_id), conn)

def find_soil_name(conn, user_soil_name):
    return pandas.read_sql('''
    SELECT * 
    FROM soils
    WHERE soil_name = "''' + str(user_soil_name) + '"', conn)

def bysoil_grounds(conn, user_soil_id):
    return pandas.read_sql('''
    SELECT grounds.ground_id, ground_name, ground_description, ground_density, ground_humidity, ground_hardness_Moos, ground_picture 
    FROM grounds 
    JOIN connection_soils_grounds ON (grounds.ground_id = connection_soils_grounds.ground_id) 
    JOIN soils ON (connection_soils_grounds.soil_id = soils.soil_id) 
    WHERE soils.soil_id = ''' + str(user_soil_id), conn)

def bysoil_grounds_noused(conn, user_soil_id):
    return pandas.read_sql('''
    SELECT DISTINCT *     
    FROM grounds 
    WHERE grounds.ground_id NOT IN 
    (SELECT DISTINCT grounds.ground_id
    FROM grounds 
    JOIN connection_soils_grounds ON (grounds.ground_id = connection_soils_grounds.ground_id) 
    JOIN soils ON (connection_soils_grounds.soil_id = soils.soil_id) 
    WHERE soils.soil_id = ''' + str(user_soil_id) + ')', conn)

def bysoil_plants(conn, user_soil_id):
    return pandas.read_sql('''
    SELECT DISTINCT plants.plant_id, plant_name, plant_description, plant_isFodder, plant_isExactingToTheLight, plant_isOneYear, plant_isTwoYears, plant_isManyYears, plant_climat, plant_required_minerals_and_trace_elements, plant_temperature_min, plant_temperature_max, plant_kingdom, plant_philum, plant_class, plant_order, plant_family, plant_genus, plant_species, plant_picture 
    FROM plants 
    JOIN connection_soils_plants ON (plants.plant_id = connection_soils_plants.plant_id) 
    JOIN soils ON (connection_soils_plants.soil_id = soils.soil_id) 
    WHERE soils.soil_id = ''' + str(user_soil_id), conn)

def bysoil_plants_noused(conn, user_soil_id):
    return pandas.read_sql('''
    SELECT DISTINCT * 
    FROM plants 
    WHERE plants.plant_id NOT IN 
    (SELECT DISTINCT plants.plant_id 
    FROM plants 
    JOIN connection_soils_plants ON (plants.plant_id = connection_soils_plants.plant_id) 
    JOIN soils ON (connection_soils_plants.soil_id = soils.soil_id) 
    WHERE soils.soil_id = ''' + str(user_soil_id) + ')', conn)

def insert_soil(conn, user_soil_name, user_soil_description):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO soils(soil_name, soil_description) 
        VALUES (:usersoilname, :usersoildescription)
        ''', {"usersoilname": user_soil_name, "usersoildescription": user_soil_description})
    conn.commit()

def delete_soil(conn, user_soil_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM soils WHERE soil_id = :soiliddelete
        ''', {"soiliddelete": user_soil_id})
    conn.commit()

def update_soil_name(conn, user_soil_id, user_soil_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE soils 
        SET soil_name = :usersoilname 
        WHERE soil_id = :usersoilid
        ''', {"usersoilid": user_soil_id, "usersoilname": user_soil_name})
    conn.commit()

def update_soil_description(conn, user_soil_id, user_soil_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE soils 
        SET soil_description = :usersoildescription 
        WHERE soil_id = :usersoilid
        ''', {"usersoilid": user_soil_id, "usersoildescription": user_soil_description})
    conn.commit()

def update_soil_acidity(conn, user_soil_id, user_soil_acidity):
    cur = conn.cursor()
    cur.execute('''
        UPDATE soils 
        SET soil_acidity = :usersoilacidity 
        WHERE soil_id = :usersoilid
        ''', {"usersoilid": user_soil_id, "usersoilacidity": user_soil_acidity})
    conn.commit()

def update_soil_minerals(conn, user_soil_id, user_soil_minerals):
    cur = conn.cursor()
    cur.execute('''
        UPDATE soils 
        SET soil_minerals = :usersoilminerals 
        WHERE soil_id = :usersoilid
        ''', {"usersoilid": user_soil_id, "usersoilminerals": user_soil_minerals})
    conn.commit()

def update_soil_profile(conn, user_soil_id, user_soil_profile):
    cur = conn.cursor()
    cur.execute('''
        UPDATE soils 
        SET soil_profile = :usersoilprofile 
        WHERE soil_id = :usersoilid
        ''', {"usersoilid": user_soil_id, "usersoilprofile": user_soil_profile})
    conn.commit()

def update_soil_picture(conn, user_soil_id, user_soil_picture):
    cur = conn.cursor()
    cur.execute('''
        UPDATE soils 
        SET soil_picture = :usersoilpicture 
        WHERE soil_id = :usersoilid
        ''', {"usersoilid": user_soil_id, "usersoilpicture": user_soil_picture})
    conn.commit()

def get_soil_picture(conn, user_soil_id):
    return pandas.read_sql('''
    SELECT soil_picture 
    FROM soils
    WHERE soil_id = ''' + str(user_soil_id), conn)
