cursor.execute("""
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    is_waiter BOOL NULL DEFAULT FALSE
);
""")
conn.commit()