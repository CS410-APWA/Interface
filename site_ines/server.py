from flask import Flask, render_template, request, url_for
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

dict =  {
    1: "Autobiographical, Paths to Prison",
    2: "Education, Re-entry, Other Programs",
    3: "Family",
    4: "Health Care",
    5: "Judicial Misconduct and Legal Remediation",
    6: "Personal/Internal Change/Coping",
    7: "Physical Conditions and Security",
    8: "Political and Intellectual Labor among IP",
    9: "Prison Culture/Community/Society",
    10: "Prison Industry/Prison as Business",
    11: "Social Alienation, Indifference, Hostility",
    12: "Staff/prison Abuse of IP"}

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_essays_with_topic(conn, topic):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute('SELECT filename FROM essays WHERE "{}" > 0 ORDER BY "{}" DESC'.format(topic, topic))

    d = {}
    count = 0
    rows = cur.fetchall()

    print("Total: ", len(rows))
    for row in rows:
        d[count] = "https://apw.dhinitiative.org/islandora/object/apw%3A" + list(row)[0][4:list(row)[0].find('.')] + "?solr_nav%5Bid%5D=de9208daa3f92a256e25&solr_nav%5Bpage%5D=0&solr_nav%5Boffset%5D=0"
        count += 1
    #   print(row)
    #print(list(rows[0]))
    return d

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get-topic/', methods=['GET', 'POST'])
def get_topic():
    database = r"db.sqlite3"
    topic = dict[int(request.form.get("myDropdown"))]
    print("=======Topic is:======= ", topic)

    # create a database connection
    conn = create_connection(database)
    with conn:
      #print("Query essays of topic {}." % topic)
      query_results = select_essays_with_topic(conn, topic)
      return query_results


if __name__ == '__main__':
  app.run(debug=True)
