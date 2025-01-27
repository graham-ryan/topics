from flask import Flask, render_template, url_for, redirect, request
from database_setup import database_setup
import duckdb
import pyarrow as pa
from nlp.bgem3_embeddings import embed

app = Flask(__name__)

conn = duckdb.connect('duckdb/topics.duckdb')
database_setup(conn)

def get_topics() -> list:
	return [x[1] for x in conn.query("""select * from topics""").fetchall()]

def get_history() -> list:
	return [x for x in conn.query("""select d.text, t.name, array_inner_product(d.embedding, t.embedding) AS similarity 
								  from documents d
								  cross join topics t  
								  order by d.id desc""").fetchall()]
	
@app.route('/')
def index():
	url_for('static', filename='style.css')
	return render_template('index.html', topics=get_topics(), history=get_history())

@app.route("/api/submit", methods=["POST"])
def handle_submit():
	text = request.form['text'].strip()
	embedding = embed(text)
	embedding_table = pa.Table.from_pydict({
        "text": [text],
        "embedding": [embedding]
    })
	conn.query(f"""INSERT INTO documents FROM (FROM embedding_table SELECT nextval('seq_document_id'), text, embedding);""")
	return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run()