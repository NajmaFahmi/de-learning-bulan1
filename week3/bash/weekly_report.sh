#!/bin/bash

##### ----- CHALLENGE ----- #####

## 1. Buat Variable
DIR_1="./linux"
DIR_2="./bash"
FILE_LOG="./bash/weekly_report.log"
TEMP_FILE="/tmp/temp_file.txt"

## 2. Buat Fungsi Log
log() {
    LEVEL=$1
    MSG=$2
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] [$LEVEL] $MSG" >> $FILE_LOG
    echo "[$TIMESTAMP] [$LEVEL] $MSG"
}

## 3. Buat Fungsi Trap
cleanup() {
    log "INFO" "Melakukan cleanup file..."
    rm -f $TEMP_FILE
    log "INFO" "Cleanup berhasil dilakukan"
}
trap cleanup EXIT

## 4. Mulai pipeline
log "INFO" "ETL Pipeline dimulai..."

## 5. Scan Folder Linux dan Hitung Isinya
if [ ! -d $DIR_1 ]; then 
    log "WARNING" "$DIR_1 tidak ditemukan"
    exit 1
fi 
log "INFO" "$DIR_1 behasil ditemukan"

TOTAL_FILES_DIR_1=$(ls $DIR_1 | wc -l | tr -d ' ' )
if [ $TOTAL_FILES_DIR_1 -eq 0 ] ; then 
    log "WARNING" "Tidak ada files di $DIR_1"
    exit 1
fi 
log "INFO" "Jumlah files di $DIR_1: $TOTAL_FILES_DIR_1"

## 6. Scan Folder Bash dan Hitung Isinya
if [ ! -d $DIR_2 ]; then 
    log "WARNING" "$DIR_2 tidak ditemukan"
    exit 1
fi 
log "INFO" "$DIR_2 behasil ditemukan"

TOTAL_FILES_DIR_2=$(ls $DIR_2 | wc -l | tr -d ' ' )
if [ $TOTAL_FILES_DIR_2 -eq 0 ]; then 
    log "WARNING" "Tidak ada files di $DIR_2"
    exit 1
fi 
log "INFO" "Jumlah files di $DIR_2: $TOTAL_FILES_DIR_2"

## 7. Bandingkan Jumlah Kedua Folder
if [ $TOTAL_FILES_DIR_1 -gt $TOTAL_FILES_DIR_2 ]; then 
    log "INFO" "File $DIR_1 lebih banyak file nya ($TOTAL_FILES_DIR_1 vs $TOTAL_FILES_DIR_2) dibanding $DIR_2"
elif [ $TOTAL_FILES_DIR_2 -gt $TOTAL_FILES_DIR_1 ]; then 
    log "INFO" "File $DIR_2 lebih banyak file nya ($TOTAL_FILES_DIR_2 vs $TOTAL_FILES_DIR_1) dibanding $DIR_1"
else 
    log "INFO" "Kedua folder memiliki jumlah file yang sama"
fi 

## 8. Tutup Pipeline
log "INFO" "ETL Pipeline selesai"
exit 0