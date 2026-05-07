from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal


# ------- LATIHAN 1 -------

# class Film(BaseModel):
#     film_id: int
#     title: str
#     rental_rate: Decimal
#     rating: Optional[str] = None 

# # Test 1: data valid
# film1 = Film(film_id = 1, title = 'Academy Dinosaur', rental_rate = 0.99)
# print(f"Valid: {film1}")

# # Test 2: coercion - string ke int
# film2 = Film(film_id = '42', title = 'Test Film', rental_rate = '4.99')
# print(f"Coerced: {film2}")

# # Test 3: data invalid - lihat apa yg terjadi
# try:
#     film3 = Film(film_id='bukan angka', title = 'Bad Film', rental_rate = 0.99)
# except Exception as e:
#     print(f"Validation error: {e}")





# ------- LATIHAN 2 -------

# buat kelas 

# class FilmValidated(BaseModel):
#     film_id: int 
#     title: str 
#     rental_rate: Decimal 
#     rating: Optional[str] = None 

#     @field_validator('rental_rate')
#     @classmethod 
#     def rental_rate_must_be_positive(cls, v):
#         if v <= 0:
#             raise ValueError(f"rental_rate harus positif, bukan: {v}")
#         return v 
    
#     @field_validator('title')
#     @classmethod 
#     def title_must_not_be_empty(cls, v):
#         if not v.strip():
#             raise ValueError("title tidak boleh kosong atau hanya spasi")
#         return v.strip()


# # test validasi
# f1 = FilmValidated(film_id = 1, title = 'Academy Dinosaur', rental_rate = 0.99)
# print(f"Valid: {f1}")

# # test rental_rate negatif
# try:
#     f2 = FilmValidated(film_id = 2, title = 'Bad Film', rental_rate = -1.00)
# except Exception as e:
#     print(f"Error: {e}")

# # test title kosong
# try:
#     f3 = FilmValidated(film_id = 3, title = "    ", rental_rate = 2.99)
# except Exception as e:
#     print(f"Error: {e}")





# ------- LATIHAN 3 -------
# ------- GABUNG PSYCOPG2 & PYDANTIC -------

import psycopg2
from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal


# KONEKSI DATABASE
def create_connection():
    try: 
        conn = psycopg2.connect(
            host = "localhost",
            database = "latihan_de",
            user = "najma",
            password = ""
        )
        return conn 
    except Exception as e:
        print(f"Koneksi gagal: {e}")
        return None 
    

# MODEL VALIDASI
class Film(BaseModel):
    film_id: int 
    title: str 
    rental_rate: Decimal 
    rating: Optional[str] = None 

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("title tidak boleh kosong atau hanya spasi")
        return v.strip()

    @field_validator('rental_rate')
    @classmethod
    def rental_rate_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError(f"rental_rate harus positif, bukan: {v}")
        return v 


# INSERT DATA MEMAKAI MODEL VALIDASI
def process_film(conn, raw_data: dict):
    try:
        film = Film(**raw_data)
        with conn.cursor() as cur:
            cur.execute("""
                insert into film_log (film_id, title)
                values (%s, %s)
                on conflict (film_id)
                do update set 
                    title = excluded.title,
                    last_updated = now()
                where film_log.title is distinct from excluded.title
            """, (film.film_id, film.title)
            )
        conn.commit()
        print(f"Berhasil: film_id {film.film_id} - {film.title}")
    except Exception as e:
        conn.rollback()
        print(f"Gagal: {raw_data} -> {e}")


# DATA SIMULASI DARI SUMBER EKSTERNAL (biasanya dari CSV atau API)
raw_films = [
    {"film_id": 10, "title": "  New Film ", "rental_rate": "2.99"},
    {"film_id": 11, "title": "Another Film", "rental_rate": 4.99},
    {"film_id": 12, "title": "   ", "rental_rate": 1.99},
    {"film_id": 13, "title": "Bad Rate Film", "rental_rate": -1.00},
    {"film_id": 10, "title": "New Film", "rental_rate": "2.99"}
]


# JALANKAN
conn = create_connection()
if conn:
    for raw in raw_films:
        process_film(conn, raw)
    conn.close()