from flask import Flask, render_template, jsonify
import os
import psycopg2

app = Flask(__name__)                                                                                                                                        
print('Hello')
#Connect to database
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn.autocommit=True
curr = conn.cursor()

i = 1
@app.route('/_data')
def chart_data():
    query = "SELECT * FROM moisture_level WHERE id=" + str(i)
    curr.execute(query)
    res = curr.fetchall()
    return jsonify(res[0])

@app.route("/")
def index():
    return render_template('index.html')
