import duckdb

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
            name VARCHAR(255)
        );
        CREATE OR REPLACE SEQUENCE seq_topic_id START 1;   
        INSERT INTO topics (id, name) VALUES
        (nextval('seq_topic_id'),'Backpacking'),
        (nextval('seq_topic_id'),'Running'),
        (nextval('seq_topic_id'),'Rock Climbing')
    """)