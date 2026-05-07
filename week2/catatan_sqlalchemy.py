from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Session
from datetime import datetime


### 1. CREATE ENGINE
engine = create_engine(
    "postgresql+psycopg2://najma@localhost/latihan_de",
    echo=True  # print semua SQL yang dijalankan — bagus untuk belajar
)


### 2. CREATE BASE CLASS UNTUK SEMUA MODEL
class Base(DeclarativeBase):
    pass


### 3. CREATE MODEL -- UNTUK TABLE film.log
class FilmLog(Base):
    __tablename__ = "film_log"
    
    film_id = Column(Integer, primary_key=True)
    title = Column(String(255))
    last_updated = Column(TIMESTAMP, default=datetime.now)
    
    def __repr__(self):
        return f"FilmLog(film_id={self.film_id}, title={self.title})"


### 4. READ TABLE
with Session(engine) as session:
    films = session.query(FilmLog).order_by(FilmLog.film_id).all()
    print("\n=== Data film_log ===")
    for film in films:
        print(film)


### 5. INSERT DATA INTO TABLE
with Session(engine) as session:
    new_film = FilmLog(film_id=50, title="SQLAlchemy Test Film")
    session.add(new_film)
    session.commit()
    print("\nInsert berhasil: film_id 50")

# Read again
with Session(engine) as session:
    film = session.query(FilmLog).filter(FilmLog.film_id == 50).first()
    print(f"\nVerifikasi: {film}")


### 6. TEST CONNECTION
with engine.connect() as conn:
    print("Koneksi berhasil")