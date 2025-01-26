from flask import Flask, render_template, url_for
from database_setup import database_setup
import duckdb

app = Flask(__name__)

conn = duckdb.connect('duckdb/topics.duckdb')
database_setup(conn)

def get_topics() -> list:
	return [x[1] for x in conn.query("""select * from topics""").fetchall()]
	

@app.route('/')
@app.route('/index')
def index():
	url_for('static', filename='style.css')
	topics = get_topics()
	return render_template('index.html', topics=topics, history=['XD'])