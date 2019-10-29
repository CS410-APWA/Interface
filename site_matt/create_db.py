import json
import os
import sqlite3

# remove database if it already exists
exists = os.path.isfile("db.sqlite3")
if exists:
    os.remove("db.sqlite3")

# connect to database
conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

# create clusters table
table = "clusters"
columns = "CLUSTER INTEGER, THEMES TEXT, TITLES TEXT, PRIMARY KEY (CLUSTER)"
c.execute("CREATE TABLE {} ({});".format(table, columns))

# example data insert
for i in range(3):
    cluster = i
    themes = [('Family', 0.005), ('Physical Conditions and Security', 0.002)]
    titles = ["essay1.txt", "essay2.txt", "essay3.txt"]
    c.execute("INSERT INTO {} VALUES ({}, '{}', '{}')".format(table,
                                                              cluster,
                                                              json.dumps(themes),
                                                              json.dumps(titles)))

# commit changes and close the connection to the database file
conn.commit()
conn.close()
