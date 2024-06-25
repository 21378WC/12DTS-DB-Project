from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "C:/Users/21378/OneDrive - Wellington College/Felix Nichols - 12DTS/Databases Term 2/12DTS DB Assessment/tags"


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

@app.route('/tags')
def render_pokemon():
    title = "Pokemon list"
    query = "SELECT * FROM pokemon_table"
    con = create_connection(DATABASE)
    with app.app_context():
        cur = con.cursor()
    cur.execute(query)
    tag_list = cur.fetchall()
    con.close()
    return render_template("pokemon_list.html", data=tag_list, title=title, types=get_types())

@app.route('/tags/<gen>')
def render_gen(gen):
    gen_value = gen
    title = 'Generation ' + gen_value + ' Pokemon'
    query = "SELECT * FROM pokemon_table WHERE Generation = ?"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (gen_value,))
    pokemon_list = cur.fetchall()
    con.close()
    return render_template("pokemon_list.html", data=pokemon_list, title=title, types=get_types())

@app.route('/<leg>')
def render_legendary(leg):
    title = "Legendary Pokemon"
    query = "SELECT * FROM pokemon_table WHERE Legendary = 1"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    pokemon_list = cur.fetchall()
    con.close()
    return render_template("pokemon_list.html", data=pokemon_list, title=title, types=get_types())

@app.route('/search', methods=['GET', 'POST'])
def render_search():
    search = request.form['search']
    title = "Search for " + search
    query = "SELECT * FROM pokemon_table WHERE Name like ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search,))
    tag_list = cur.fetchall()
    con.close()
    return render_template("pokemon_list.html", data=tag_list, title=title, types=get_types())


if __name__ == '__main__':
    app.run(debug=True)


