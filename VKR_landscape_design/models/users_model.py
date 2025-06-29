import pandas as pd

def get_users(conn, is_need_pictures=False):
    users = pd.read_sql('''
        SELECT * FROM users
    ''', conn)

    if is_need_pictures:
        for index, row in users.iterrows():
            picture_id = row['user_picture_id']
            if pd.notna(picture_id):
                picture = pd.read_sql(f'''
                    SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
                ''', conn)
                if not picture.empty:
                    users.at[index, 'user_picture_base64'] = picture.iloc[0]['picture_base64']
            else:
                users.at[index, 'user_picture_base64'] = None

    return users

def get_one_user(conn, user_id, is_need_pictures=False):
    user = pd.read_sql(f'''
        SELECT * FROM users WHERE user_id = {user_id}
    ''', conn)

    if user.empty:
        return user

    if is_need_pictures:
        picture_id = user.iloc[0]['user_picture_id']
        if pd.notna(picture_id):
            picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {picture_id}
            ''', conn)
            if not picture.empty:
                user.at[0, 'user_picture_base64'] = picture.iloc[0]['picture_base64']
        else:
            user.at[0, 'user_picture_base64'] = None

    return user

def find_user_login(conn, user_login):
    return pd.read_sql(f'''
        SELECT user_id
        FROM users
        WHERE user_login = "{user_login}"
    ''', conn)

def find_user_login_with_id(conn, user_id, user_login):
    return pd.read_sql(f'''
        SELECT user_id
        FROM users
        WHERE user_login = "{user_login}" AND user_id != {user_id}
    ''', conn)

def insert_user(conn, user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_is_admin, user_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO users(user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_is_admin, user_picture_id)
        VALUES (:userlogin, :userpassword, :useremail, :usersurname, :username, :userfathername, :userage, :userisfemale, :userisadmin, :userpictureid)
    ''', {
        "userlogin": user_login,
        "userpassword": user_password,
        "useremail": user_email,
        "usersurname": user_surname,
        "username": user_name,
        "userfathername": user_fathername,
        "userage": user_age,
        "userisfemale": user_is_female,
        "userisadmin": user_is_admin,
        "userpictureid": user_picture_id
    })
    conn.commit()

def delete_user(conn, user_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM users
        WHERE user_id = :userid
    ''', {"userid": user_id})
    conn.commit()

def update_user(conn, user_id, user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_is_admin, user_picture_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users
        SET
            user_login = CASE WHEN :userlogin IS NOT NULL THEN :userlogin ELSE user_login END,
            user_password = CASE WHEN :userpassword IS NOT NULL THEN :userpassword ELSE user_password END,
            user_email = CASE WHEN :useremail IS NOT NULL THEN :useremail ELSE user_email END,
            user_surname = CASE WHEN :usersurname IS NOT NULL THEN :usersurname ELSE user_surname END,
            user_name = CASE WHEN :username IS NOT NULL THEN :username ELSE user_name END,
            user_fathername = CASE WHEN :userfathername IS NOT NULL THEN :userfathername ELSE user_fathername END,
            user_age = CASE WHEN :userage IS NOT NULL THEN :userage ELSE user_age END,
            user_is_female = CASE WHEN :userisfemale IS NOT NULL THEN :userisfemale ELSE user_is_female END,
            user_is_admin = CASE WHEN :userisadmin IS NOT NULL THEN :userisadmin ELSE user_is_admin END,
            user_picture_id = CASE WHEN :userpictureid IS NOT NULL THEN :userpictureid ELSE user_picture_id END
        WHERE user_id = :userid
    ''', {
        "userid": user_id,
        "userlogin": user_login,
        "userpassword": user_password,
        "useremail": user_email,
        "usersurname": user_surname,
        "username": user_name,
        "userfathername": user_fathername,
        "userage": user_age,
        "userisfemale": user_is_female,
        "userisadmin": user_is_admin,
        "userpictureid": user_picture_id
    })
    conn.commit()
