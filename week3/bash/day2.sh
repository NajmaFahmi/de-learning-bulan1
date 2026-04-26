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










########## ---------- PRAKTEK ---------- ##########
## "pipeline_check.sh"

### 1. DEFINE VARIABLES
LOG_FILE="pipeline.log"
STATUS="success"
TOTAL_FILES=0

echo "" > $LOG_FILE

### 2. CREATE FUNCTION
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> $LOG_FILE
}

### 3. JALANKAN FUNCTION (process dimulai)
log "Pipeline dimulai"

### 4. JALANKAN FUNCTION (check keberadaan file)
for FILE in *.csv; do 
    if [ -f "$FILE" ]; then 
        log "Memproses: $FILE"
        TOTAL_FILES=$((TOTAL_FILES + 1))
    fi 
done 

### 5. JALANKAN FUNCTION (check apakah ada file yg terproses)
if [ $TOTAL_FILES -eq 0 ]; then 
    STATUS="warning"
    log "Tidak ada file CSV ditemukan"
else 
    log "Total file diproses: $TOTAL_FILES"
fi 


### 6. CHECK VARIABLE AKHIR (HASIL)
log "Pipeline selesai dengan status: $STATUS"
echo "Selesai. Cek $LOG_FILE untuk detail"










########## ---------- TANTANGAN ---------- ##########
## monitor.sh

### 1. CARI FOLDER
DIREKTORI="linux"

if [ -d "$DIREKTORI" ]; then
    echo "$DIREKTORI ditemukan"
else 
    echo "Error! $DIREKTORI tidak ditemukan"
    exit 1
fi 


### 2. HITUNG FILES
TOTAL_FILES=0
for file in $DIREKTORI/*; do 
    echo "$file"
    TOTAL_FILES=$((TOTAL_FILES + 1))
done

## atau

TOTAL_FILES=0
TOTAL_FILES=$(ls $DIREKTORI | wc -l)


### 3. TULIS HASIL AKHIR
echo "Ditemukan $TOTAL_FILES file di direktori $DIREKTORI" > ./bash/monitor.log
