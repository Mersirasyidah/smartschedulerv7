import pandas as pd
from database import load_database

db = load_database()

guru = db["Guru"]

# -----------------------------------
# Membuat slot jadwal kosong
# -----------------------------------

jadwal = {}

HARI = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat"
]

JAM = {

    "Senin":[1,2,3,4,5,6,7,8,9],

    "Selasa":[1,2,3,4,5,6,7,8,9],

    "Rabu":[1,2,3,4,5,6,7,8,9],

    "Kamis":[1,2,3,4,5,6,7,8,9],

    "Jumat":[1,2,3,4,5,6]

}

def buat_slot_jadwal():

    jadwal = {}

    kelas = set()

    for item in guru["Kelas"]:

        for k in item.split(","):

            kelas.add(k.strip())

    for k in kelas:

        jadwal[k] = {}

        for hari in HARI:

            jadwal[k][hari] = {}

            for jam in JAM[hari]:

                jadwal[k][hari][jam] = None

    return jadwal

def boleh_mengajar(guru_row,hari,jam):

    hari_mgmp = guru_row["Hari MGMP"]

    if hari == hari_mgmp:

        if jam >= 5:

            return False

    return True

kelas = item.split(",")

pembagian = [2,2,1]

# -----------------------------------
# Program Utama
# -----------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print(" SMART SCHEDULER V7")
    print("=" * 50)

    jadwal = buat_slot_jadwal()

    print("\nSlot jadwal berhasil dibuat.\n")

    print("Jumlah kelas :", len(jadwal))

    print("\nDaftar kelas:")

    for kelas in sorted(jadwal.keys()):
        print("-", kelas)

    print("\nScheduler siap dijalankan...")


