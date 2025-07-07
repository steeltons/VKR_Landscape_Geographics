import pandas as pd

def get_territories(conn, search_query=None, page=None, elements=None):
    offset = 0
    if page is not None and elements is not None:
        offset = (page - 1) * elements

    query = '''
        SELECT territorie_id, territorie_landscape_id, territorie_description, territorie_color_r, territorie_color_g, territorie_color_b
        FROM territories
    '''

    if search_query:
        query += f'''
            WHERE territorie_description LIKE '%{search_query}%'
        '''

    if elements is not None:
        query += f' LIMIT {elements} OFFSET {offset}'

    territories = pd.read_sql(query, conn)

    return territories

def get_one_territorie(conn, user_territorie_id):
    return pd.read_sql(f'''
        SELECT territorie_id, territorie_landscape_id, territorie_description, territorie_color_r, territorie_color_g, territorie_color_b
        FROM territories
        WHERE territorie_id = {user_territorie_id}
    ''', conn)

def insert_territorie(conn, user_territorie_landscape_id, user_territorie_description, user_territorie_color_r, user_territorie_color_g, user_territorie_color_b):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO territories(territorie_landscape_id, territorie_description, territorie_color_r, territorie_color_g, territorie_color_b)
        VALUES (:userterritorielandscapeid, :userterritoriedescription, :userterritoriecolorr, :userterritoriecolorg, :userterritoriecolorb)
    ''', {
        "userterritorielandscapeid": user_territorie_landscape_id,
        "userterritoriedescription": user_territorie_description,
        "userterritoriecolorr": user_territorie_color_r,
        "userterritoriecolorg": user_territorie_color_g,
        "userterritoriecolorb": user_territorie_color_b
    })
    conn.commit()
    return cur.lastrowid


def delete_territorie(conn, user_territorie_id):
    cur = conn.cursor()
    cur.execute('''
        DELETE FROM territories
        WHERE territorie_id = :territorieid
    ''', {"territorieid": user_territorie_id})
    conn.commit()

def update_territorie(conn, user_territorie_id, user_territorie_landscape_id, user_territorie_description, user_territorie_color_r, user_territorie_color_g, user_territorie_color_b):
    cur = conn.cursor()
    cur.execute('''
        UPDATE territories
        SET
            territorie_landscape_id = :userterritorielandscapeid,
            territorie_description = :userterritoriedescription,
            territorie_color_r = :userterritoriecolorr,
            territorie_color_g = :userterritoriecolorg,
            territorie_color_b = :userterritoriecolorb
        WHERE territorie_id = :userterritorieid
    ''', {
        "userterritorieid": user_territorie_id,
        "userterritorielandscapeid": user_territorie_landscape_id,
        "userterritoriedescription": user_territorie_description,
        "userterritoriecolorr": user_territorie_color_r,
        "userterritoriecolorg": user_territorie_color_g,
        "userterritoriecolorb": user_territorie_color_b
    })
    conn.commit()


def untie_landscape_from_territorie(conn, user_territorie_id):
    cur = conn.cursor()
    cur.execute('''
        UPDATE territories
        SET
            territorie_landscape_id = NULL
        WHERE territorie_id = :userterritorieid
    ''', {
        "userterritorieid": user_territorie_id
    })
    conn.commit()

def get_coords_by_territorie_id(conn, territorie_id):
    return pd.read_sql(f'''
        SELECT coords_id, coords_coord_x, coords_coord_y, coords_order 
        FROM coords 
        WHERE coords_territorie_id = {territorie_id} 
        ORDER BY coords_order ASC
    ''', conn)


def is_point_in_polygon(point_x, point_y, polygon_coords):
    """
    Определяет, находится ли точка внутри многоугольника, используя алгоритм лучевого пересечения.

    :param point_x: Координата X точки.
    :param point_y: Координата Y точки.
    :param polygon_coords: Список кортежей с координатами вершин многоугольника.
    :return: True, если точка внутри многоугольника, иначе False.
    """
    n = len(polygon_coords)
    inside = False
    p1x, p1y = polygon_coords[0]
    for i in range(n + 1):
        p2x, p2y = polygon_coords[i % n]
        if point_y > min(p1y, p2y):
            if point_y <= max(p1y, p2y):
                if point_x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (point_y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or point_x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def get_territorie_with_related_objects(conn, territorie_id, is_need_pictures=False):
    # Получаем информацию о территории
    territorie = get_one_territorie(conn, territorie_id)
    if len(territorie) == 0:
        return None

    territorie_data = territorie.to_dict(orient="records")[0]
    landscape_id = territorie_data['territorie_landscape_id']

    if not landscape_id:
        return None

    # Получаем информацию о ландшафте
    landscape = pd.read_sql(f'''
        SELECT * FROM landscapes WHERE landscape_id = {landscape_id}
    ''', conn)

    if len(landscape) == 0:
        return None

    landscape_data = landscape.to_dict(orient="records")[0]

    # Получаем связанные объекты
    soils = pd.read_sql(f'''
        SELECT s.* FROM soils s
        JOIN connections_landscapes_soils c ON s.soil_id = c.soil_id
        WHERE c.landscape_id = {landscape_id}
    ''', conn)

    grounds = pd.read_sql(f'''
        SELECT g.* FROM grounds g
        JOIN connections_landscapes_grounds c ON g.ground_id = c.ground_id
        WHERE c.landscape_id = {landscape_id}
    ''', conn)

    plants = pd.read_sql(f'''
        SELECT p.* FROM plants p
        JOIN connections_landscapes_plants c ON p.plant_id = c.plant_id
        WHERE c.landscape_id = {landscape_id}
    ''', conn)

    reliefs = pd.read_sql(f'''
        SELECT r.* FROM reliefs r
        JOIN connections_landscapes_reliefs c ON r.relief_id = c.relief_id
        WHERE c.landscape_id = {landscape_id}
    ''', conn)

    foundations = pd.read_sql(f'''
        SELECT f.* FROM foundations f
        JOIN connections_landscapes_foundations c ON f.foundation_id = c.foundation_id
        WHERE c.landscape_id = {landscape_id}
    ''', conn)

    waters = pd.read_sql(f'''
        SELECT w.* FROM waters w
        JOIN connections_landscapes_waters c ON w.water_id = c.water_id
        WHERE c.landscape_id = {landscape_id}
    ''', conn)

    climats = pd.read_sql(f'''
        SELECT c.* FROM climats c
        JOIN connections_landscapes_climats cl ON c.climat_id = cl.climat_id
        WHERE cl.landscape_id = {landscape_id}
    ''', conn)

    # Если нужно возвращать картинки, добавляем их в результаты
    if is_need_pictures:
        # Получаем картинки для ландшафта
        if 'landscape_picture_id' in landscape_data and landscape_data['landscape_picture_id']:
            landscape_picture = pd.read_sql(f'''
                SELECT picture_base64 FROM pictures WHERE picture_id = {landscape_data['landscape_picture_id']}
            ''', conn)
            if not landscape_picture.empty:
                landscape_data['landscape_picture_base64'] = landscape_picture.iloc[0]['picture_base64']

        # Получаем картинки для почв
        if not soils.empty and 'soil_picture_id' in soils.columns:
            soil_picture_ids = soils['soil_picture_id'].dropna().unique()
            soil_pictures = {}
            for pid in soil_picture_ids:
                picture = pd.read_sql(f'''
                    SELECT picture_id, picture_base64 FROM pictures WHERE picture_id = {int(pid)}
                ''', conn)
                if not picture.empty:
                    soil_pictures[pid] = picture.iloc[0]['picture_base64']
            soils['soil_picture_base64'] = soils['soil_picture_id'].map(soil_pictures)

        # Получаем картинки для грунтов
        if not grounds.empty and 'ground_picture_id' in grounds.columns:
            ground_picture_ids = grounds['ground_picture_id'].dropna().unique()
            ground_pictures = {}
            for pid in ground_picture_ids:
                picture = pd.read_sql(f'''
                    SELECT picture_id, picture_base64 FROM pictures WHERE picture_id = {int(pid)}
                ''', conn)
                if not picture.empty:
                    ground_pictures[pid] = picture.iloc[0]['picture_base64']
            grounds['ground_picture_base64'] = grounds['ground_picture_id'].map(ground_pictures)

        # Получаем картинки для растений
        if not plants.empty and 'plant_picture_id' in plants.columns:
            plant_picture_ids = plants['plant_picture_id'].dropna().unique()
            plant_pictures = {}
            for pid in plant_picture_ids:
                picture = pd.read_sql(f'''
                    SELECT picture_id, picture_base64 FROM pictures WHERE picture_id = {int(pid)}
                ''', conn)
                if not picture.empty:
                    plant_pictures[pid] = picture.iloc[0]['picture_base64']
            plants['plant_picture_base64'] = plants['plant_picture_id'].map(plant_pictures)

        # Получаем картинки для рельефов
        if not reliefs.empty and 'relief_picture_id' in reliefs.columns:
            relief_picture_ids = reliefs['relief_picture_id'].dropna().unique()
            relief_pictures = {}
            for pid in relief_picture_ids:
                picture = pd.read_sql(f'''
                    SELECT picture_id, picture_base64 FROM pictures WHERE picture_id = {int(pid)}
                ''', conn)
                if not picture.empty:
                    relief_pictures[pid] = picture.iloc[0]['picture_base64']
            reliefs['relief_picture_base64'] = reliefs['relief_picture_id'].map(relief_pictures)

        # Получаем картинки для фундаментов
        if not foundations.empty and 'foundation_picture_id' in foundations.columns:
            foundation_picture_ids = foundations['foundation_picture_id'].dropna().unique()
            foundation_pictures = {}
            for pid in foundation_picture_ids:
                picture = pd.read_sql(f'''
                    SELECT picture_id, picture_base64 FROM pictures WHERE picture_id = {int(pid)}
                ''', conn)
                if not picture.empty:
                    foundation_pictures[pid] = picture.iloc[0]['picture_base64']
            foundations['foundation_picture_base64'] = foundations['foundation_picture_id'].map(foundation_pictures)

        # Получаем картинки для вод
        if not waters.empty and 'water_picture_id' in waters.columns:
            water_picture_ids = waters['water_picture_id'].dropna().unique()
            water_pictures = {}
            for pid in water_picture_ids:
                picture = pd.read_sql(f'''
                    SELECT picture_id, picture_base64 FROM pictures WHERE picture_id = {int(pid)}
                ''', conn)
                if not picture.empty:
                    water_pictures[pid] = picture.iloc[0]['picture_base64']
            waters['water_picture_base64'] = waters['water_picture_id'].map(water_pictures)

        # Получаем картинки для климатов
        if not climats.empty and 'climat_picture_id' in climats.columns:
            climat_picture_ids = climats['climat_picture_id'].dropna().unique()
            climat_pictures = {}
            for pid in climat_picture_ids:
                picture = pd.read_sql(f'''
                    SELECT picture_id, picture_base64 FROM pictures WHERE picture_id = {int(pid)}
                ''', conn)
                if not picture.empty:
                    climat_pictures[pid] = picture.iloc[0]['picture_base64']
            climats['climat_picture_base64'] = climats['climat_picture_id'].map(climat_pictures)

    # Возвращаем все данные
    return {
        "territorie": territorie_data,
        "landscape": landscape_data,
        "soils": soils.to_dict(orient="records"),
        "grounds": grounds.to_dict(orient="records"),
        "plants": plants.to_dict(orient="records"),
        "reliefs": reliefs.to_dict(orient="records"),
        "foundations": foundations.to_dict(orient="records"),
        "waters": waters.to_dict(orient="records"),
        "climats": climats.to_dict(orient="records")
    }