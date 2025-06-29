import sqlite3
import pandas as pd
import numpy as np
from models.animals_model import *
from models.grounds_model import *
from models.plants_model import *
from models.soils_model import *
from models.territories_model import *
from models.users_model import *
from models.connection_territories_soils_model import *
from models.connection_landscapes_foundations_model import *
from models.connection_landscapes_grounds_model import *
from models.connection_landscapes_climats_model import *
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100

# PRAGMA FOREIGN_KEYS = on;

con = sqlite3.connect("VKR.sqlite")
con.commit()

cursor = con.cursor()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
cursor.execute("SELECT * FROM territories")
print(cursor.fetchall())
cursor.execute("SELECT * FROM soils")
print(cursor.fetchall())
cursor.execute("SELECT * FROM plants")
print(cursor.fetchall())
cursor.execute("SELECT * FROM grounds")
print(cursor.fetchall())

print()





print()
print('--------------------')
print()

#print(get_plants(con))
#insert_plant(con, 'qqq', 'www', 'eee')
#delete_plant(con, 6)
#update_plant_name(con, 7, 'IVAN!')
#print(get_plants(con))

print(get_one_user(con, 1))
print(get_one_user_without_password(con, 1))
print(authorisation(con, 'lutiysidor', 'abracadabra123'))

print('-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-')
print(bycoord(con, 43.10562, 131.87353))
print('-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-')
print(get_connection_plants_animals(con))
print(find_connection_plants_animals_plant_id(con, 5, 1))
print(bycoord(con, 43.10562, 131.87353))

print(check_one_plants_temperature_min_max_min(con, 1, 3))
print(check_one_plants_temperature_min_max_max(con, 1, 0))

print('111111')
print(byplant_animals(con, 5))
print('222222')
print(byplant_animals_noused(con, 5))
print('333333')

print()
print('--------------------')
print()