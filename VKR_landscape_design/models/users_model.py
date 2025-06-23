import pandas
import hashlib
import os
import bcrypt

def get_users(conn):
    return pandas.read_sql('''
    SELECT user_id, user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_isFemale, user_picture, user_isAdmin 
    FROM users
    ''', conn)

def get_users_without_password(conn):
    return pandas.read_sql('''
    SELECT user_id, user_login, user_email, user_surname, user_name, user_fathername, user_age, user_isFemale, user_picture, user_isAdmin
    FROM users
    ''', conn)

def get_users_without_password_admins(conn):
    return pandas.read_sql('''
    SELECT user_id, user_login, user_email, user_surname, user_name, user_fathername, user_age, user_isFemale, user_picture
    FROM users
    WHERE user_isAdmin = TRUE
    ''', conn)

def get_users_without_password_noadmins(conn):
    return pandas.read_sql('''
    SELECT user_id, user_login, user_email, user_surname, user_name, user_fathername, user_age, user_isFemale, user_picture
    FROM users
    WHERE user_isAdmin = FALSE
    ''', conn)

def get_one_user(conn, user_user_id):
    return pandas.read_sql('''
    SELECT user_id, user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_isFemale, user_isAdmin 
    FROM users 
    WHERE user_id = ''' + str(user_user_id), conn)

def find_user_login(conn, user_user_login):
    return pandas.read_sql('''
    SELECT * 
    FROM users
    WHERE user_login = "''' + str(user_user_login) + '"', conn)

def find_user_email(conn, user_user_email):
    return pandas.read_sql('''
    SELECT * 
    FROM users
    WHERE user_email = "''' + str(user_user_email) + '"', conn)

def get_one_user_without_password(conn, user_user_id):
    return pandas.read_sql('''
    SELECT user_id, user_login, user_email, user_surname, user_name, user_fathername, user_age, user_isFemale, user_isAdmin 
    FROM users 
    WHERE user_id = ''' + str(user_user_id), conn)

def authorisation(conn, user_user_login, user_user_password):
    h = hashlib.md5(user_user_password.encode('utf8'))
    p = h.hexdigest()
    return pandas.read_sql('''
    SELECT user_id, user_isAdmin
    FROM users
    WHERE user_login = "''' + user_user_login + '" AND user_password = "' + str(p) + '"', conn)

def insert_user(conn, user_user_login, user_user_password, user_user_email):
    h = hashlib.md5(user_user_password.encode('utf8'))
    p = h.hexdigest()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO users(user_login, user_password, user_email, user_isAdmin) VALUES (:userlogin, :userpassword, :useremail, FALSE)
        ''', {"userlogin": user_user_login, "userpassword": p, "useremail": user_user_email})
    conn.commit()

def delete_user(conn, user_user_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM users WHERE user_id = :useriddelete
        ''', {"useriddelete": user_user_id})
    conn.commit()

def update_user_login(conn, user_user_id, user_user_login):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_login = :userlogin 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "userlogin": user_user_login})
    conn.commit()

def update_user_password(conn, user_user_id, user_user_password):
    h = hashlib.md5(user_user_password.encode('utf8'))
    p = h.hexdigest()
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_password = :userpassword 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "userpassword": p})
    conn.commit()

def update_user_email(conn, user_user_id, user_user_email):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_email = :useremail 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "useremail": user_user_email})
    conn.commit()

def update_user_surname(conn, user_user_id, user_user_surname):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_surname = :usersurname 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "usersurname": user_user_surname})
    conn.commit()

def update_user_name(conn, user_user_id, user_user_name):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_name = :username 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "username": user_user_name})
    conn.commit()

def update_user_fathername(conn, user_user_id, user_user_fathername):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_fathername = :userfathername 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "userfathername": user_user_fathername})
    conn.commit()

def update_user_age(conn, user_user_id, user_user_age):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_age = :userage 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "userage": user_user_age})
    conn.commit()

def update_user_isFemale(conn, user_user_id, user_user_isFemale):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_isFemale = :userisFemale 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "userisFemale": user_user_isFemale})
    conn.commit()

def update_user_picture(conn, user_user_id, user_user_picture):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_picture = :userpicture 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "userpicture": user_user_picture})
    conn.commit()

def update_user_isAdmin(conn, user_user_id, user_user_isAdmin):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users 
        SET user_isAdmin = :userisAdmin 
        WHERE user_id = :useridupdate
        ''', {"useridupdate": user_user_id, "userisAdmin": user_user_isAdmin})
    conn.commit()

def get_user_picture(conn, user_user_id):
    return pandas.read_sql('''
    SELECT user_picture 
    FROM users
    WHERE user_id = ''' + str(user_user_id), conn)
