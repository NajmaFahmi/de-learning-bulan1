from src.extractor import extract_films, extract_rentals 
from src.models import FilmRecord, RentalRecord
from typing import List


#### ~~~~ TESTING FOR FILM DATA ~~~~

### 1. Test 1
## extract_films() mengembalikan 1000 records
def test_extract_films():
    # jalankan fungsi
    result = extract_films()

    # verifikasi hasil
    assert len(result) == 1000


### 2. Test 2
## extract_rentals() mengembalikan 16044 records
def test_extract_rentals():
    # jalankan fungsi
    result = extract_rentals()

    # verifikasi hasil
    assert len(result) == 16044


### 3. Test 3
## fungsi memiliki output instance FilmRecord / RentalRecord
def test_output_record():
    # jalankan fungsi
    films = extract_films()
    rentals = extract_rentals()

    # verifikasi hasil untuk film
    assert all(isinstance(f, FilmRecord) for f in films)
    assert all(isinstance(r, RentalRecord) for r in rentals)