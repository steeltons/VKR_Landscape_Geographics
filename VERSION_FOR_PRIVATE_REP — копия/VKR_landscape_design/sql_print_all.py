import sqlite3
from models.users_model import *
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