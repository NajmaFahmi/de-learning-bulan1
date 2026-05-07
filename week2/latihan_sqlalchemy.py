from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Session
from datetime import datetime


#### ENGINE (connection) ####
## jembatan antar python dan database
engine = create_engine(
    "postgresql+psycopg2://najma@localhost/latihan_de",
    echo = False #ganti True kalau mau lihat yg terjadi di background sistem saat running
)


#### MODEL (class) ####
## class = tabel
# Base class untuk semua model
class Base(DeclarativeBase):
    pass 

# Model tabel film_log
class FilmLog(Base):
    __tablename__ = "film_log"

    film_id = Column(Integer, primary_key = True)
    title = Column(String(255))
    last_updated = Column(TIMESTAMP, default = datetime.now)

    def __repr__(self):
        return f"FilmLog(film_id = {self.film_id}, title = {self.title})"


#### TEST KONEKSI ####
with engine.connect() as conn:
    print("Koneksi Berhasil")


#### READ ####
## read a table
with Session(engine) as session:
    films = session.query(FilmLog).order_by(FilmLog.film_id).all()
    print("\n=== Data Tabel film_log ===")
    for film in films:
        print(film)


#### WRITE ####
## insert data into a table
with Session(engine) as session:
    new_film = FilmLog(film_id = 50, title = "SQLAlchemy Test Film")
    session.add(new_film)
    session.commit()
    print("\nInsert berhasil: film_id 50")


## Read - baca kembali
with Session(engine) as session:
    film = session.query(FilmLog).filter(FilmLog.film_id == 50).first()
    print(f"\nVerifikasi: {film}")