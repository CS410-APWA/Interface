import json
import os
import sqlite3
import joblib
import requests
from bs4 import BeautifulSoup

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
columns = "filename, title, " + ', '.join(['"' + x + '"' for x in themes])
c.execute("CREATE TABLE {} ({});".format(table, columns))

# example data insert
for essay, themeList in essayThemeDict.items():
    print(essay)
    themeDict = dict(themeList)
    themeVals = ''
    try:
        title = BeautifulSoup(requests.get("https://apw.dhinitiative.org/islandora/object/apw%3A" + essay[4:essay.find('.')] + "?").text).find('h1').text
    except:
    	continue
    for theme in themes:
	    if theme in themeDict.keys():
	        themeVals += ', ' + str(themeDict[theme])
	    else:
	        themeVals += ', 0'

    c.execute("INSERT INTO {} VALUES ('{}', '{}'{})".format(table,
                                                      essay,
                                                      title.replace("'", "''"), 
                                                      themeVals))

# commit changes and close the connection to the database file
conn.commit()
conn.close()
