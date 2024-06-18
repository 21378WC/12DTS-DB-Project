from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "C:/Users/21378/OneDrive - Wellington College/Felix Nichols - 12DTS/Databases Term 2/12DTS DB Assessment/pokemon_db"

def create_connection(db_file):
    """
    Creates a connection to the database
    :parameter db_file: - the name of the file
    :return:   connection - a connection to the database
    """

    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None



def get_types():
    con = create_connection(DATABASE)
    query = "SELECT DISTINCT * FROM pokemon_table ORDER BY id DESC"
    cur = con.cursor()
    cur.execute(query)
    types = cur.fetchall()
    #print(types)
    for i in range(len(types)):
        types[i] = types[i][0]
    #print(types)
    return types

@app.route('/')
def render_home():
    return render_template("home_page.html")

@app.route('/tags/<tag_type>')
def render_webpages(tag_type):
    title = "Pokemon list"
    query = "SELECT tag, description FROM pokemon_table WHERE type = ?"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (tag_type, ))
    tag_list = cur.fetchall()
    print(tag_list)
    con.close()
    return render_template("page.html", data=tag_list, title=title, types=get_types())

@app.route('/search', methods=['GET', 'POST'])
def render_search():
    search = request.form['search']
    title = "Search for " + search
    query = "SELECT Name FROM pokemon_db WHERE Name like ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search))
    tag_list = cur.fetchall()
    print(tag_list)
    con.close()

    return render_template("page.html", data=tag_list, title=title, types=get_types())


if __name__ == '__main__':
    app.run(debug=True)

#@app.route('/styles')
#def render_styles():
#    query = "SELECT tag, description FROM html_tags WHERE type='CSS'"
#    con = create_connection(DATABASE)
#    print(con)
#    cur = con.cursor()
#    # Query the database
#    cur.execute(query)
#    tag_list = cur.fetchall()
#    con.close()
#    print(tag_list)
#    return render_template("page.html", tag=tag_list)


