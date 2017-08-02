#sqlite3
import sqlite3 

# Connecting to the database file
sqlite_file = 'players.db'
column_name = 'firstname'
table_name = "players"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# 1) Contents of all columns for row that match a certain value in 1 column
c.execute('SELECT * FROM {tn} WHERE {cn}="Stephen"'.\
        format(tn=table_name, cn=column_name))
all_rows = c.fetchall()
print type(all_rows)
print('1):', all_rows)