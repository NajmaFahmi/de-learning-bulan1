#!/bin/bash


########## ---------- MATERI ---------- ##########

## -- PRINT
echo "Hello dari script pertamaku"


## -- VARIABLES
NAMA="Najma"
HARI="selasa"
TAHUN="2026"

echo "Halo, ini $NAMA, hari ini $HARI tahun $TAHUN"


## -- CONDITIONALS
SUHU=17

if [ $SUHU -gt 30 ]; then
    echo "Panas, nyalakan AC"
elif [ $SUHU -gt 20 ]; then 
    echo "Suhu normal"
else
    echo "Dingin, pakai jaket"
fi


STATUS="success"

if [ "$STATUS" = "success" ]; then
    echo "Pipeline berhasil"
fi


## -- LOOPS
# - for loop
for FILE in *.csv; do
    echo "Memproses file: $FILE"
done 

# - while loop
COUNTER=1

while [ $COUNTER -le 5 ]; do 
    echo "Iterasi ke-$COUNTER"
    COUNTER=$((COUNTER + 1))
done 


## -- FUNCTIONS 
check_file() {
    if [ -f "$1" ]; then        #apakah argumen pertama yg dikirim ada atau tidak
        echo "File $1 ditemukan"
    else 
        echo "File $1 TIDAK ditemukan"
    fi
}

check_file "latihan.sh"  #apakah data ini ada
check_file "data.csv"


## -- STDIN, STDOUT, STDERR
# - masuk ke stdout
echo "Ini sukses"

# - masuk ke stderr
echo "Ini error" >&2

# - keluar dari
echo -p "Masukkan nama: "

