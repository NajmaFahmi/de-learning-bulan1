import psycopg2
from psycopg2 import OperationalError



### A. MEMBUAT CONNECTION
def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="latihan_de",
            user="najma",
            password=""
        )
        print("Koneksi berhasil")
        return conn
    except OperationalError as e:
        print(f"Koneksi gagal: {e}")
        return None

conn = create_connection()
if conn:
    conn.close()
    print("Koneksi ditutup")





### B. MEMBACA DATABASE
def fetch_films(conn, limit=5):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT film_id, title, rental_rate
            FROM film
            ORDER BY film_id
            LIMIT %s
        """, (limit,))
        results = cur.fetchall()
        for row in results:
            print(f"ID: {row[0]} | Title: {row[1]} | Rate: {row[2]}")
    return results

conn = create_connection()
if conn:
    fetch_films(conn)
    conn.close()
    print("Koneksi ditutup")





### C. INSERT DATA INTO TABLE
def insert_film_log(conn, film_id, title, rental_rate):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO film_log (film_id, title)
            VALUES (%s, %s)
            ON CONFLICT (film_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                last_updated = NOW()
            WHERE film_log.title IS DISTINCT FROM EXCLUDED.title
        """, (film_id, title))
    conn.commit()
    print(f"film_id {film_id} berhasil diproses")

conn = create_connection()
if conn:
    fetch_films(conn)
    
    insert_film_log(conn, 1, 'Academy Dinosaur', 0.99)
    insert_film_log(conn, 1, 'Academy Dinosaur', 0.99)  # dijalankan 2x
    insert_film_log(conn, 99, 'Film Baru', 2.99)
    
    conn.close()
    print("Koneksi ditutup")

## check hasil di dbeaver
# SELECT * FROM film_log ORDER BY film_id;