# !/bin/bash


##### ----- TRAP ----- #####

# Buat variable
TEMP_FILE="/tmp/pipeline_temp.csv"

# Buat fungsi TRAP
cleanup() {
    echo "Membersihkan file..."
    rm -f $TEMP_FILE 
    echo "Cleanup Selesai"
}

# Jalankan trap
trap cleanup EXIT            # jalankan fungsi cleanup saat script selesai
trap cleanup ERR            # jalankan fungsi cleanup saat ada error





##### ----- LOGGING ----- #####

# Buat Variable
LOG_FILE="pipeline.log"
LOG_LEVEL="INFO"

# Buat fungsi LOG
log() {
    local LEVEL=$1
    local MESSAGE=$2
    local TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] [$LEVEL] $MESSAGE" >> $LOG_FILE
    echo "[$TIMESTAMP] [$LEVEL] $MESSAGE"
}

# Jalankan fungsi
log "INFO" "Pipeline dimulai"
log "WARNING" "File CSV tidak ditemukan, skip"
log "ERROR" "Koneksi database gagal"
log "INFO" "Pipeline selesai"





##### ----- EXIT CODES ----- #####

# Buat conditionals EXIT
if [ ! -f "data.csv" ]; then        #jika file tsb tidak ditemukan
    echo "File tidak ditemukan"
    exit 1                          #error, stop disini
fi 

echo "Proses selesai"               #kalau masuk kesini berarti sukses
exit 0                              #sukses

# Cek apakah sukses atau tidak
echo $?                             # 0 = sukses, non-zero = error
