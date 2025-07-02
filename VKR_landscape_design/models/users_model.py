import pandas as pd

def get_users(conn, is_need_pictures=False, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT * FROM users 
        ORDER BY user_surname ASC, user_name ASC, user_fathername ASC, user_email ASC, user_login ASC
    '''

    if search_query:
        query += f'''
            WHERE user_surname LIKE '%{search_query}%'
            OR user_name LIKE '%{search_query}%'
            OR user_fathername LIKE '%{search_query}%'
            OR user_login LIKE '%{search_query}%'
            OR user_email LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    users = pd.read_sql(query, conn)

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

def delete_user(conn, user_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM users
        WHERE user_id = :userid
    ''', {"userid": user_id})
    conn.commit()

def insert_user(conn, user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_picture_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO users(user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_picture_id)
        VALUES (:userlogin, :userpassword, :useremail, :usersurname, :username, :userfathername, :userage, :userisfemale, :userpictureid)
    ''', {
        "userlogin": user_login,
        "userpassword": user_password,
        "useremail": user_email,
        "usersurname": user_surname,
        "username": user_name,
        "userfathername": user_fathername,
        "userage": user_age,
        "userisfemale": user_is_female,
        "userpictureid": user_picture_id
    })
    conn.commit()

def update_user(conn, user_id, user_login, user_password, user_email, user_surname, user_name, user_fathername, user_age, user_is_female, user_picture_id):
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
        "userpictureid": user_picture_id
    })
    conn.commit()

def update_user_set_admin(conn, user_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users
        SET
            user_is_admin = 'true'
        WHERE user_id = :userid
    ''', {
        "userid": user_id
    })
    conn.commit()

def update_user_set_notadmin(conn, user_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE users
        SET
            user_is_admin = NULL
        WHERE user_id = :userid
    ''', {
        "userid": user_id
    })
    conn.commit()
