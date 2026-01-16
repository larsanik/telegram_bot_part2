import psycopg2

conn=psycopg2.connect(
    host='localhost',
    port=5432,
    database='ice_cream',
    user='user1',
    password='password1')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    is_waiter BOOL NULL DEFAULT FALSE
);
""")
conn.commit()