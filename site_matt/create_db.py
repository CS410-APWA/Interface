import json
import os
import sqlite3
import joblib

# remove database if it already exists
exists = os.path.isfile("db.sqlite3")
if exists:
    os.remove("db.sqlite3")

# connect to database
conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

essayThemeDict = joblib.load('essayThemeDict.joblib')
themes = joblib.load('theme_index.joblib').keys()

# create clusters table
table = "essays"
columns = "filename, " + ', '.join(['"' + x + '"' for x in themes])
c.execute("CREATE TABLE {} ({});".format(table, columns))

# example data insert
for essay, themeList in essayThemeDict.items():
    themeDict = dict(themeList)
    themeVals = ''
    for theme in themes:
    	if theme in themeDict.keys():
    		themeVals += ', ' + str(themeDict[theme])
    	else:
    		themeVals += ', 0'

    c.execute("INSERT INTO {} VALUES ('{}'{})".format(table,
                                                      essay,
                                                      themeVals))

# commit changes and close the connection to the database file
conn.commit()
conn.close()
