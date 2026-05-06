#!/bin/bash


#### ----- PRAKTEK ----- #####

## 1. Buat Variable
LOG_FILE="etl.log"
TEMP_FILE="/tmp/etl_temp.txt"

## 2. Buat Fungsi Log (tulis logging)
log() {
    local LEVEL=$1
    local MSG=$2
    local TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] [$LEVEL] $MSG" | tee -a $LOG_FILE
}

## 3. Buat Fungsi Trap (membersihkan file)
cleanup() {
    log "INFO" "Menjalankan cleanup..."
    rm -f $TEMP_FILE
    log "INFO" "Cleanup selesai"
}
trap cleanup EXIT       #jalankan saat file sudah selesai

### ----

## 1. Jalankan pipeline
log "INFO" "ETL Pipeline dimulai"

## 2. Tulis data di temporary file
echo "raw, data, simulasi" > $TEMP_FILE
echo "old, new, updated" >> $TEMP_FILE

## 3. Check apakah file benar terbuat
if [ ! -f "$TEMP_FILE" ]; then 
    log "ERROR" "Gagal membuat temporary file"
    exit 1              # kalau gagal berhenti disini
fi 
log "INFO" "Temporary file berhasil dibuat"     #k alau berhasil, lanjut terus

## 4. Check berapa baris yg ada di file
# BARIS=$(wc -l < $TEMP_FILE | tr -d ' ')
## atau
BARIS=$(cat $TEMP_FILE | wc -l | tr -d ' ')
log "INFO" "Total baris diproses: $BARIS"

## 5. Tutup pipeline
log "INFO" "ETL pipeline selesai"
exit 0





##### ----- TANTANGAN ----- #####

## 1. Buat Variable
LOG_FILE="./bash/tantangan.log"
TEMP_FILE="/tmp/temp_file.txt"
DIRECTORY="./linux"         #atau "linux" juga bisa

## 2. Buat Fungsi Log
log() {
    local LEVEL=$1
    local MESSAGE=$2
    local TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] [$LEVEL] $MESSAGE" >> $LOG_FILE
    echo "[$TIMESTAMP] [$LEVEL] $MESSAGE"
}

## 3. Buat Fungsi cleanup
cleanup() {
    log "INFO" "Cleanup dipanggil oleh: EXIT"
    log "INFO" "Melakukan cleanup..."
    rm -f $TEMP_FILE
    log "INFO" "Cleanup selesai"
}
trap cleanup EXIT

## ------------

## 1. Mulai pipeline
log "INFO" "ETL Pipeline dimulai..."

## 2. Check apakah folder linux ada
if [ ! -d $DIRECTORY ]; then
    log "ERROR" "Directory tidak ditemukan"
    exit 1
fi 
log "INFO" "Directory ditemukan"

## 3. Hitung jumlah files di folder tsb
TOTAL_FILES=$(ls $DIRECTORY | wc -l | tr -d ' ' )

## 4. Buat conditionals jumlah files
if [ $TOTAL_FILES -eq 0 ]; then
    log "WARNING" "Tidak ada file di directory"
    exit 1
fi 
log "INFO" "Jumlah files di folder $DIRECTORY : $TOTAL_FILES"

## 5. Tutup pipeline
log "INFO" "ETL Pipeline selesai"
exit 0
