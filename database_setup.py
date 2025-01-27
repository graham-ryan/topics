from nlp.bgem3_embeddings import embed
import pyarrow as pa

def database_setup(conn):
    """Nukes and recreates the database at topics.duckdb"""
    conn.query("""
        CREATE OR REPLACE TABLE documents (
            id INTEGER PRIMARY KEY,
            text VARCHAR(255),
            embedding FLOAT[1024]
        );
        CREATE OR REPLACE SEQUENCE seq_document_id START 1;
                      
        CREATE OR REPLACE TABLE topics (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            embedding FLOAT[1024]
        );
        CREATE OR REPLACE SEQUENCE seq_topic_id START 1;   
               
        CREATE OR REPLACE TABLE similarity_scores (
            document_id INTEGER,
            topic_id INTEGER,
            score FLOAT
        );
    """)

    base_topics = ["Backpacking", "Running", "Rock Climbing"]
    
    for topic in base_topics:
        embedding = embed(topic)
        embedding_table = pa.Table.from_pydict({
            "name": [topic],
            "embedding": [embedding]
        })
        conn.query(f"""INSERT INTO topics FROM (FROM embedding_table SELECT nextval('seq_topic_id'), name, embedding);""")

