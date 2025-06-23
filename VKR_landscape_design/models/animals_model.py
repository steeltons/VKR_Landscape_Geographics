import pandas

def get_animals(conn):
    return pandas.read_sql('''
    SELECT animal_id, animal_name, animal_description, animal_kingdom, animal_philum, animal_class, animal_order, animal_family, animal_genus, animal_species, animal_picture  
    FROM animals
    ''', conn)

def find_animal_name(conn, user_animal_name):
    return pandas.read_sql('''
    SELECT * 
    FROM animals
    WHERE animal_name = "''' + str(user_animal_name) + '"', conn)

def get_one_animal(conn, user_animal_id):
    return pandas.read_sql('''
    SELECT animal_id, animal_name, animal_description, animal_kingdom, animal_philum, animal_class, animal_order, animal_family, animal_genus, animal_species 
    FROM animals 
    WHERE animal_id = ''' + str(user_animal_id), conn)

def insert_animal(conn, user_animal_name, user_animal_description):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO animals(animal_name, animal_description) 
        VALUES (:useranimalname, :useranimaldescription)
        ''', {"useranimalname": user_animal_name, "useranimaldescription": user_animal_description})
    conn.commit()

def delete_animal(conn, user_animal_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM animals WHERE animal_id = :animaliddelete
        ''', {"animaliddelete": user_animal_id})
    conn.commit()

def update_animal_name(conn, user_animal_id, user_animal_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_name = :useranimalname 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalname": user_animal_name})
    conn.commit()

def update_animal_description(conn, user_animal_id, user_animal_description):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_description = :useranimaldescription 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimaldescription": user_animal_description})
    conn.commit()

def update_animal_kingdom(conn, user_animal_id, user_animal_kingdom):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_kingdom = :useranimalkingdom 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalkingdom": user_animal_kingdom})
    conn.commit()

def update_animal_philum(conn, user_animal_id, user_animal_philum):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_philum = :useranimalphilum 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalphilum": user_animal_philum})
    conn.commit()

def update_animal_class(conn, user_animal_id, user_animal_class):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_class = :useranimalclass 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalclass": user_animal_class})
    conn.commit()

def update_animal_order(conn, user_animal_id, user_animal_order):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_order = :useranimalorder 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalorder": user_animal_order})
    conn.commit()

def update_animal_family(conn, user_animal_id, user_animal_family):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_family = :useranimalfamily 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalfamily": user_animal_family})
    conn.commit()

def update_animal_genus(conn, user_animal_id, user_animal_genus):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_genus = :useranimalgenus 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalgenus": user_animal_genus})
    conn.commit()

def update_animal_species(conn, user_animal_id, user_animal_species):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_species = :useranimalspecies 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalspecies": user_animal_species})
    conn.commit()

def update_animal_picture(conn, user_animal_id, user_animal_picture):
    cur = conn.cursor()
    cur.execute('''
        UPDATE animals 
        SET animal_picture = :useranimalpicture 
        WHERE animal_id = :useranimalid
        ''', {"useranimalid": user_animal_id, "useranimalpicture": user_animal_picture})
    conn.commit()

def get_animal_picture(conn, user_animal_id):
    return pandas.read_sql('''
    SELECT animal_picture 
    FROM animals
    WHERE animal_id = ''' + str(user_animal_id), conn)