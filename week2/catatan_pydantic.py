from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


### A. CREATE ONLY BASE MODEL
class Film(BaseModel):
    film_id: int
    title: str
    rental_rate: Decimal
    rating: Optional[str] = None

# Test 1: data valid
film1 = Film(film_id=1, title="Academy Dinosaur", rental_rate=0.99)
print(f"Valid: {film1}")

# Test 2: coercion - string ke int
film2 = Film(film_id="42", title="Test Film", rental_rate="4.99")
print(f"Coerced: {film2}")

# Test 3: data invalid - lihat apa yang terjadi
try:
    film3 = Film(film_id="bukan_angka", title="Bad Film", rental_rate=0.99)
except Exception as e:
    print(f"Validation error: {e}")





### B. CREATE CUSTOM VALIDATOR
class FilmValidated(BaseModel):
    film_id: int
    title: str
    rental_rate: Decimal
    rating: Optional[str] = None

    @field_validator('rental_rate')
    @classmethod
    def rental_rate_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError(f"rental_rate harus positif, dapat: {v}")
        return v

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("title tidak boleh kosong atau hanya spasi")
        return v.strip()

# Test valid
f1 = FilmValidated(film_id=1, title="  Academy Dinosaur  ", rental_rate=0.99)
print(f"Valid: {f1}")

# Test rental_rate negatif
try:
    f2 = FilmValidated(film_id=2, title="Bad Film", rental_rate=-1.00)
except Exception as e:
    print(f"Error: {e}")

# Test title kosong
try:
    f3 = FilmValidated(film_id=3, title="   ", rental_rate=2.99)
except Exception as e:
    print(f"Error: {e}")





### D. COMBINE PYSCOPG2 & PYDANTIC (MINI PIPELINE)
import psycopg2
from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal

# Model validasi
class Film(BaseModel):
    film_id: int
    title: str
    rental_rate: Decimal
    rating: Optional[str] = None

    @field_validator('rental_rate')
    @classmethod
    def rental_rate_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError(f"rental_rate harus positif, dapat: {v}")
        return v

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("title tidak boleh kosong atau hanya spasi")
        return v.strip()

# Koneksi database
def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="latihan_de",
            user="najma",
            password=""
        )
        return conn
    except Exception as e:
        print(f"Koneksi gagal: {e}")
        return None

# Insert dengan validasi
def process_film(conn, raw_data: dict):
    try:
        film = Film(**raw_data)
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO film_log (film_id, title)
                VALUES (%s, %s)
                ON CONFLICT (film_id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    last_updated = NOW()
                WHERE film_log.title IS DISTINCT FROM EXCLUDED.title
            """, (film.film_id, film.title))
        conn.commit()
        print(f"Berhasil: film_id {film.film_id} - {film.title}")
    except Exception as e:
        conn.rollback()
        print(f"Gagal: {raw_data} → {e}")

# Data simulasi dari sumber eksternal (bisa dari CSV atau API)
raw_films = [
    {"film_id": 10, "title": "  New Film  ", "rental_rate": "2.99"},
    {"film_id": 11, "title": "Another Film", "rental_rate": 4.99},
    {"film_id": 12, "title": "   ", "rental_rate": 1.99},      # title kosong
    {"film_id": 13, "title": "Bad Rate Film", "rental_rate": -1.00},  # rate negatif
    {"film_id": 10, "title": "New Film", "rental_rate": "2.99"},  # duplikat
]

conn = create_connection()
if conn:
    for raw in raw_films:
        process_film(conn, raw)
    conn.close()