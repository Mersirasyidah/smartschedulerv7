"""
==============================================================
SMART SCHEDULER V7
Versi 1.0

Scheduler Engine

Bagian 1
- Import Library
- Membaca Database
- Konfigurasi
- Membuat Slot Jadwal
==============================================================
"""

import random
import copy
import pandas as pd

from database import load_database

# ==========================================================
# LOAD DATABASE
# ==========================================================

db = load_database()

guru = db["Guru"]

guru_mengajar = db["Guru_Mengajar"]

rombel = db["Rombel"]

hari_jam = db["Hari_Jam"]

# ==========================================================
# KONFIGURASI HARI
# ==========================================================

HARI = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat"
]

# ==========================================================
# SLOT JP
# ==========================================================

JP = {

    "Senin":9,

    "Selasa":9,

    "Rabu":9,

    "Kamis":9,

    "Jumat":6

}

# ==========================================================
# MEMBUAT SLOT JADWAL
# ==========================================================

def buat_jadwal_kosong():

    jadwal = {}

    daftar_kelas = sorted(

        rombel["Kelas"].unique()

    )

    for kelas in daftar_kelas:

        jadwal[kelas] = {}

        for hari in HARI:

            jadwal[kelas][hari] = {}

            for jp in range(1, JP[hari]+1):

                jadwal[kelas][hari][jp] = None

    return jadwal

# ==========================================================
# DAFTAR KELAS
# ==========================================================

def daftar_kelas():

    return sorted(

        rombel["Kelas"].unique()

    )

# ==========================================================
# DAFTAR GURU
# ==========================================================

def daftar_guru():

    return sorted(

        guru["Nama Guru"].unique()

    )

# ==========================================================
# DAFTAR MAPEL
# ==========================================================

def daftar_mapel():

    return sorted(

        guru_mengajar["Mapel"].unique()

    )

# ==========================================================
# PARSER PEMBAGIAN JP
# ==========================================================

def pembagian_jp(data):

    if pd.isna(data):

        return []

    data = str(data)

    data = data.replace(" ", "")

    if data == "":

        return []

    hasil = []

    for item in data.split(","):

        try:

            hasil.append(int(float(item)))

        except:

            pass

    return hasil

# ==========================================================
# PARSER KELAS
# ==========================================================

def parser_kelas(teks):

    if pd.isna(teks):

        return []

    teks = str(teks)

    hasil = []

    for item in teks.split(","):

        item = item.strip()

        if item != "":

            hasil.append(item)

    return hasil

# ==========================================================
# PARSER MAPEL
# ==========================================================

def parser_mapel(teks):

    if pd.isna(teks):

        return []

    teks = str(teks)

    hasil = []

    for item in teks.split(","):

        item = item.strip()

        if item != "":

            hasil.append(item)

    return hasil

# ==========================================================
# MEMBUAT DATA MENGAJAR
# ==========================================================

def buat_data_mengajar():

    data = []

    for _, row in guru_mengajar.iterrows():

        kelas_list = parser_kelas(row["Kelas"])

        mapel_list = parser_mapel(row["Mapel"])

        pembagian = pembagian_jp(row["Pembagian"])

        for kelas in kelas_list:

            for mapel in mapel_list:

                data.append({

                    "ID Guru": row["ID Guru"],

                    "Guru": row["Nama Guru"],

                    "Mapel": mapel,

                    "Kelas": kelas,

                    "JP": int(row["JP"]),

                    "Pembagian": pembagian,

                    "Prioritas": int(row["Prioritas"]),

                    "Hari MGMP": row["Hari MGMP"]

                })

    data = pd.DataFrame(data)

    data = data.sort_values(

        by=[

            "Prioritas",

            "Guru",

            "Mapel",

            "Kelas"

        ]

    )

    return data.reset_index(drop=True)

# ==========================================================
# CEK DATABASE
# ==========================================================

def info_database():

    print("="*60)

    print("SMART SCHEDULER V7")

    print("="*60)

    print()

    print("Guru :", len(guru))

    print("Guru Mengajar :", len(guru_mengajar))

    print("Rombel :", len(rombel))

    print("Hari :", len(HARI))

    print()

    print("Jumlah Kelas :", len(daftar_kelas()))

    print("Jumlah Guru :", len(daftar_guru()))

    print()

# ==========================================================
# MEMBUAT DATA
# ==========================================================

DATA_MENGAJAR = buat_data_mengajar()

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    info_database()

    jadwal = buat_jadwal_kosong()

    print()

    print("Jumlah Data Mengajar :", len(DATA_MENGAJAR))

    print()

    print(DATA_MENGAJAR.head())

    print()

    print("Slot Jadwal Berhasil Dibuat")

    print(jadwal.keys())

# ==========================================================
# BAGIAN 2
# VALIDASI PENEMPATAN JADWAL
# ==========================================================

# ----------------------------------------------------------
# CEK APAKAH SLOT KELAS MASIH KOSONG
# ----------------------------------------------------------

def slot_kosong(jadwal, kelas, hari, jp):

    return jadwal[kelas][hari][jp] is None


# ----------------------------------------------------------
# CEK APAKAH GURU SUDAH MENGAJAR
# ----------------------------------------------------------

def guru_bentrok(jadwal, guru, hari, jp):

    for kelas in jadwal:

        isi = jadwal[kelas][hari][jp]

        if isi is None:
            continue

        if isi["Guru"] == guru:
            return True

    return False


# ----------------------------------------------------------
# HITUNG JUMLAH JP GURU PER HARI
# ----------------------------------------------------------

def jumlah_jp_guru(jadwal, guru, hari):

    jumlah = 0

    for kelas in jadwal:

        for jp in jadwal[kelas][hari]:

            isi = jadwal[kelas][hari][jp]

            if isi is None:
                continue

            if isi["Guru"] == guru:
                jumlah += 1

    return jumlah


# ----------------------------------------------------------
# CEK HARI MGMP
# ----------------------------------------------------------

def melanggar_mgmp(guru_row, hari):

    mgmp = str(guru_row["Hari MGMP"]).strip()

    if mgmp == "":
        return False

    return mgmp.lower() == hari.lower()


# ----------------------------------------------------------
# CEK APAKAH BLOK JP MUAT
# ----------------------------------------------------------

def blok_muatan(jadwal, kelas, hari, jp_awal, panjang):

    jp_terakhir = JP[hari]

    if jp_awal + panjang - 1 > jp_terakhir:
        return False

    for jp in range(jp_awal, jp_awal + panjang):

        if not slot_kosong(jadwal, kelas, hari, jp):
            return False

    return True


# ----------------------------------------------------------
# TEMPATKAN BLOK JP
# ----------------------------------------------------------

def isi_blok(

    jadwal,

    guru,

    mapel,

    kelas,

    hari,

    jp_awal,

    panjang

):

    for jp in range(jp_awal, jp_awal + panjang):

        jadwal[kelas][hari][jp] = {

            "Guru": guru,

            "Mapel": mapel,

            "JP": jp

        }


# ----------------------------------------------------------
# HAPUS BLOK
# ----------------------------------------------------------

def hapus_blok(

    jadwal,

    kelas,

    hari,

    jp_awal,

    panjang

):

    for jp in range(jp_awal, jp_awal + panjang):

        jadwal[kelas][hari][jp] = None


# ----------------------------------------------------------
# CEK APAKAH GURU MASIH BOLEH MENGAJAR
# ----------------------------------------------------------

def guru_boleh_mengajar(

    jadwal,

    guru_row,

    hari,

    jp,

    panjang

):

    guru = guru_row["Nama Guru"]

    if guru_bentrok(jadwal, guru, hari, jp):
        return False

    if melanggar_mgmp(guru_row, hari):
        return False

    jp_hari = jumlah_jp_guru(jadwal, guru, hari)

    if jp_hari + panjang > 8:
        return False

    return True


# ----------------------------------------------------------
# CEK PENEMPATAN SATU BLOK
# ----------------------------------------------------------

def boleh_ditempatkan(

    jadwal,

    guru_row,

    kelas,

    hari,

    jp_awal,

    panjang

):

    if not blok_muatan(

        jadwal,

        kelas,

        hari,

        jp_awal,

        panjang

    ):

        return False

    if not guru_boleh_mengajar(

        jadwal,

        guru_row,

        hari,

        jp_awal,

        panjang

    ):

        return False

    return True


# ==========================================================
# TEST VALIDASI
# ==========================================================

if __name__ == "__main__":

    jadwal = buat_jadwal_kosong()

    print()

    print("TEST VALIDASI")

    print()

    print(

        slot_kosong(

            jadwal,

            daftar_kelas()[0],

            "Senin",

            1

        )

    )

