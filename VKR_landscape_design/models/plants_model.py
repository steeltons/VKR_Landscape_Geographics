import pandas

def get_plants(conn):
    return pandas.read_sql('''
    SELECT plant_id, plant_name, plant_description, plant_isFodder, plant_isExactingToTheLight, plant_isOneYear, plant_isTwoYears, plant_isManyYears, plant_climat, plant_required_minerals_and_trace_elements, plant_temperature_min, plant_temperature_max, plant_kingdom, plant_philum, plant_class, plant_order, plant_family, plant_genus, plant_species, plant_picture 
    FROM plants''', conn)

def get_one_plant(conn, user_plant_id):
    return pandas.read_sql('''
    SELECT plant_id, plant_name, plant_description, plant_isFodder, plant_isExactingToTheLight, plant_isOneYear, plant_isTwoYears, plant_isManyYears, plant_climat, plant_required_minerals_and_trace_elements, plant_temperature_min, plant_temperature_max, plant_kingdom, plant_philum, plant_class, plant_order, plant_family, plant_genus, plant_species 
    FROM plants 
    WHERE plant_id = ''' + str(user_plant_id), conn)

def find_plant_name(conn, user_plant_name):
    return pandas.read_sql('''
    SELECT * 
    FROM plants
    WHERE plant_name = "''' + str(user_plant_name) + '"', conn)

def get_plants_isFodder(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM plants
    WHERE plant_isFodder = True
    ''', conn)

def check_one_plants_isFodder(conn, user_plant_id):
    return pandas.read_sql('''
    SELECT * 
    FROM plants 
    WHERE plant_isFodder = True 
    AND plant_id = ''' + str(user_plant_id), conn)


def check_one_plants_temperature_min_max_min(conn, user_plant_id, new_min):
    return pandas.read_sql('''
    SELECT *
    FROM plants 
    WHERE plant_id = ''' + str(user_plant_id) +
    ' AND (' + str(new_min) + ' <= plant_temperature_max)', conn)

def check_one_plants_temperature_min_max_max(conn, user_plant_id, new_max):
    return pandas.read_sql('''
    SELECT *
    FROM plants 
    WHERE plant_id = ''' + str(user_plant_id) +
    ' AND (plant_temperature_min <=' + str(new_max) + ')', conn)

def get_plants_isNoFodder(conn):
    return pandas.read_sql('''
    SELECT * 
    FROM plants
    WHERE plant_isFodder = False
    ''', conn)

def byplant_animals(conn, user_plant_id):
    return pandas.read_sql('''
    SELECT DISTINCT animals.animal_id, animal_name, animal_description, animal_kingdom, animal_philum, animal_class, animal_order, animal_family, animal_genus, animal_species, animal_picture 
    FROM plants
    JOIN connection_plants_animals ON (plants.plant_id = connection_plants_animals.plant_id) 
    JOIN animals ON (connection_plants_animals.animal_id = animals.animal_id)
    WHERE plants.plant_id = ''' + str(user_plant_id), conn)

def byplant_animals_noused(conn, user_plant_id):
    return pandas.read_sql('''
    SELECT DISTINCT * 
    FROM animals 
    WHERE animals.animal_id NOT IN 
    (SELECT DISTINCT animals.animal_id
    FROM animals 
    JOIN connection_plants_animals ON (animals.animal_id = connection_plants_animals.animal_id) 
    JOIN plants ON (connection_plants_animals.plant_id = plants.plant_id) 
    WHERE plants.plant_id = ''' + str(user_plant_id) + ')', conn)

def insert_plant(conn, user_plant_name, user_plant_description, user_plant_isFodder):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO plants(plant_name, plant_description, plant_isFodder) 
        VALUES (:userplantname, :userplantdescription, :userplantisFodder)
        ''', {"userplantname": user_plant_name, "userplantdescription": user_plant_description, "userplantisFodder": user_plant_isFodder})
    conn.commit()

def delete_plant(conn, user_plant_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM plants WHERE plant_id = :plantiddelete
        ''', {"plantiddelete": user_plant_id})
    conn.commit()

def update_plant_name(conn, user_plant_id, user_plant_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_name = :userplantname 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantname": user_plant_name})
    conn.commit()

def update_plant_description(conn, user_plant_id, user_plant_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_description = :userplantdescription 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantdescription": user_plant_description})
    conn.commit()

def update_plant_isFodder(conn, user_plant_id, user_plant_isFodder):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_isFodder = :userplantisFodder 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantisFodder": user_plant_isFodder})
    conn.commit()

def update_plant_isExactingToTheLight(conn, user_plant_id, user_plant_isExactingToTheLight):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_isExactingToTheLight = :userplantisExactingToTheLight 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantisExactingToTheLight": user_plant_isExactingToTheLight})
    conn.commit()

def update_plant_isOneYear(conn, user_plant_id, user_plant_isOneYear):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_isOneYear = :userplantisOneYear 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantisOneYear": user_plant_isOneYear})
    conn.commit()

def update_plant_isTwoYears(conn, user_plant_id, user_plant_isTwoYears):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_isTwoYears = :userplantisTwoYears 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantisTwoYears": user_plant_isTwoYears})
    conn.commit()

def update_plant_isManyYears(conn, user_plant_id, user_plant_isManyYears):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_isManyYears = :userplantisManyYears 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantisManyYears": user_plant_isManyYears})
    conn.commit()

def update_plant_climat(conn, user_plant_id, user_plant_climat):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_climat = :userplantclimat 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantclimat": user_plant_climat})
    conn.commit()

def update_plant_required_minerals_and_trace_elements(conn, user_plant_id, user_plant_required_minerals_and_trace_elements):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_required_minerals_and_trace_elements = :userplantrequired_minerals_and_trace_elements 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantrequired_minerals_and_trace_elements": user_plant_required_minerals_and_trace_elements})
    conn.commit()

def update_plant_temperature_min(conn, user_plant_id, user_plant_temperature_min):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_temperature_min = :userplanttemperature_min 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplanttemperature_min": user_plant_temperature_min})
    conn.commit()

def update_plant_temperature_max(conn, user_plant_id, user_plant_temperature_max):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_temperature_max = :userplanttemperature_max 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplanttemperature_max": user_plant_temperature_max})
    conn.commit()

def update_plant_kingdom(conn, user_plant_id, user_plant_kingdom):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_kingdom = :userplantkingdom 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantkingdom": user_plant_kingdom})
    conn.commit()

def update_plant_philum(conn, user_plant_id, user_plant_philum):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_philum = :userplantphilum 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantphilum": user_plant_philum})
    conn.commit()

def update_plant_class(conn, user_plant_id, user_plant_class):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_class = :userplantclass 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantclass": user_plant_class})
    conn.commit()

def update_plant_order(conn, user_plant_id, user_plant_order):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_order = :userplantorder 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantorder": user_plant_order})
    conn.commit()

def update_plant_family(conn, user_plant_id, user_plant_family):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_family = :userplantfamily 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantfamily": user_plant_family})
    conn.commit()

def update_plant_genus(conn, user_plant_id, user_plant_genus):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_genus = :userplantgenus 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantgenus": user_plant_genus})
    conn.commit()

def update_plant_species(conn, user_plant_id, user_plant_species):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_species = :userplantspecies 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantspecies": user_plant_species})
    conn.commit()

def update_plant_picture(conn, user_plant_id, user_plant_picture):
    cur = conn.cursor()
    cur.execute('''
        UPDATE plants 
        SET plant_picture = :userplantpicture 
        WHERE plant_id = :userplantid
        ''', {"userplantid": user_plant_id, "userplantpicture": user_plant_picture})
    conn.commit()

def get_plant_picture(conn, user_plant_id):
    return pandas.read_sql('''
    SELECT plant_picture 
    FROM plants
    WHERE plant_id = ''' + str(user_plant_id), conn)