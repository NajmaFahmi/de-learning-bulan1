from src.transformer import transform_films, transform_rentals
from src.models import FilmRecord, RentalRecord
from datetime import datetime
from decimal import Decimal



#### ~~~~ TESTING FOR FILM DATA ~~~~

### 1. Test 1
## film < 60 menit --> duration_category = "Short"
def test_duration_short():
    # create test data 
    data = FilmRecord(
        film_id = 1,
        title = "Test Film",
        description = "Test",
        release_year = 2026,
        rental_duration = 3,
        rental_rate = Decimal("0.99"),
        length = 45,     # < 60 --> short
        rating = "PG"
    )

    # jalankan fungsi yg akan di test
    result = transform_films([data])

    # verifikasi hasil
    assert result[0]['duration_category'] == "Short"


### 2. Test 2
## film 60-120 menit --> duration_category = "Medium"
def test_duration_medium():
    # create test data 
    data = FilmRecord(
        film_id = 1,
        title = "Test Film",
        description = "Test",
        release_year = 2026,
        rental_duration = 3,
        rental_rate = Decimal("0.99"),
        length = 100,     # 60 - 120 --> Medium
        rating = "PG"
    )

    # jalankan fungsi yg akan di test
    result = transform_films([data])

    # verifikasi hasil
    assert result[0]['duration_category'] == "Medium"


### 3. Test 3
## film > 120 menit --> duration_category = "Long"
def test_duration_long():
    # create test data 
    data = FilmRecord(
        film_id = 1,
        title = "Test Film",
        description = "Test",
        release_year = 2026,
        rental_duration = 3,
        rental_rate = Decimal("0.99"),
        length = 121,     # > 120 --> Long
        rating = "PG"
    )

    # jalankan fungsi yg akan di test
    result = transform_films([data])

    # verifikasi hasil
    assert result[0]['duration_category'] == "Long"


### 4. Test 4
## rating dinormalisasi --> uppercase dan strip whitespace
def test_rating_normalized():
    # create test data 
    data = FilmRecord(
        film_id = 1,
        title = "Test Film",
        description = "Test",
        release_year = 2026,
        rental_duration = 3,
        rental_rate = Decimal("0.99"),
        length = 121,
        rating = " NC-17"      # hasilnya harus uppercase tanpa spasi
    )

    # jalankan fungsi yg akan di test
    result = transform_films([data])

    # verifikasi hasil
    assert result[0]['rating'] == "NC-17"


### 5. Test 5
## rental_rate >= 3.99 --> is_premium = True
def test_rentalrate_premium():
    # create test data 
    data = FilmRecord(
        film_id = 1,
        title = "Test Film",
        description = "Test",
        release_year = 2026,
        rental_duration = 3,
        rental_rate = Decimal("4.00"),  # > 3.99 --> True
        length = 75,     
        rating = "PG"
    )

    # jalankan fungsi yg akan di test
    result = transform_films([data])

    # verifikasi hasil
    assert result[0]['is_premium'] == True


### 6. Test 6
## rental_rate < 3.99 --> is_premium = False
def test_rentalrate_not_premium():
    # create test data 
    data = FilmRecord(
        film_id = 1,
        title = "Test Film",
        description = "Test",
        release_year = 2026,
        rental_duration = 3,
        rental_rate = Decimal("2.99"),  # < 3.99 --> False
        length = 75,     
        rating = "PG"
    )

    # jalankan fungsi yg akan di test
    result = transform_films([data])

    # verifikasi hasil
    assert result[0]['is_premium'] == False 



#### ~~~~ TESTING FOR RENTAL DATA ~~~~

### 1. Test 1
## rental dengan return_date --> is_returned = True, rental_duration_days terisi
def test_return_true():
    # create test data 
    data = RentalRecord(
        rental_id = 1,
        rental_date = datetime(2026, 1, 1, 7, 0, 0),
        inventory_id = 120,
        customer_id = 1,
        return_date = datetime.now(),   # --> is_returned = True, rental_duration is not None
        staff_id = 1
    )

    # jalankan fungsi yg akan di test
    result = transform_rentals([data])

    # verifikasi hasil
    assert result[0]['is_returned'] == True
    assert result[0]['rental_duration_days'] is not None 


### 2. Test 2
## rental dengan return_date NONE --> is_returned = False, rental_duration_days None
def test_return_false():
    # create test data 
    data = RentalRecord(
        rental_id = 1,
        rental_date = datetime(2026, 1, 1, 7, 0, 0),
        inventory_id = 120,
        customer_id = 1,
        return_date = None,   # --> is_returned = False, rental_duration is None
        staff_id = 1
    )

    # jalankan fungsi yg akan di test
    result = transform_rentals([data])

    # verifikasi hasil
    assert result[0]['is_returned'] == False
    assert result[0]['rental_duration_days'] is None 