from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
    name = request.form['name']
    age = request.form['age']
    city = request.form['city']

    db = connect_db()
    db.execute('INSERT INTO civil_data (name, age, city) VALUES (?, ?, ?)', [name, age, city])
    db.commit()
    db.close()
    return 'Dados adicionados com sucesso!'

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    db = connect_db()
    cur = db.execute('SELECT * FROM civil_data WHERE name LIKE ? OR city LIKE ?', ['%' + query + '%', '%' + query + '%'])
    results = cur.fetchall()
    db.close()

    return render_template('search_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
