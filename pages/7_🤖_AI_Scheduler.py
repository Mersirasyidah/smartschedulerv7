import pandas as pd
from database import load_database

# =====================================
# LOAD DATABASE
# =====================================

db = load_database()

guru = db["Guru"]
mengajar = db["Guru_Mengajar"]
rombel = db["Rombel"]
hari_jam = db["Hari_Jam"]

# =====================================
# HARI BELAJAR
# =====================================

HARI = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat"
]

# =====================================
# SLOT JAM
# =====================================

JAM = {

    "Senin":[1,2,3,4,5,6,7,8,9],

    "Selasa":[1,2,3,4,5,6,7,8,9],

    "Rabu":[1,2,3,4,5,6,7,8,9],

    "Kamis":[1,2,3,4,5,6,7,8,9],

    "Jumat":[1,2,3,4,5,6]

}

# =====================================
# MEMBUAT SLOT JADWAL
# =====================================

def buat_slot_jadwal():

    jadwal = {}

    daftar_kelas = sorted(
        rombel["Kelas"].unique()
    )

    for kelas in daftar_kelas:

        jadwal[kelas] = {}

        for hari in HARI:

            jadwal[kelas][hari] = {}

            for jam in JAM[hari]:

                jadwal[kelas][hari][jam] = None

    return jadwal

# =====================================
# DAFTAR GURU
# =====================================

def daftar_guru():

    return guru["Nama Guru"].tolist()

# =====================================
# DAFTAR KELAS
# =====================================

def daftar_kelas():

    return sorted(
        rombel["Kelas"].tolist()
    )

# =====================================
# DATA MENGAJAR GURU
# =====================================

def guru_mengajar(id_guru):

    return mengajar[
        mengajar["ID Guru"] == id_guru
    ]

# =====================================
# CEK HARI MGMP
# =====================================

def hari_mgmp(id_guru):

    data = guru[
        guru["ID Guru"] == id_guru
    ]

    if len(data)==0:

        return None

    return data.iloc[0]["Hari MGMP"]

# =====================================
# CEK PRIORITAS
# =====================================

def prioritas(id_guru):

    data = guru[
        guru["ID Guru"] == id_guru
    ]

    if len(data)==0:

        return 3

    return data.iloc[0]["Prioritas"]

# =====================================
# CEK BOLEH MENGAJAR
# =====================================

def boleh_mengajar(id_guru,hari,jam):

    mgmp = hari_mgmp(id_guru)

    if hari == mgmp:

        if jam >=5:

            return False

    return True

# =====================================
# MENAMPILKAN SLOT
# =====================================

def tampilkan_slot(jadwal):

    for kelas in jadwal:

        print("="*60)

        print(kelas)

        print("="*60)

        for hari in jadwal[kelas]:

            print(hari)

            for jam in jadwal[kelas][hari]:

                print(
                    jam,
                    jadwal[kelas][hari][jam]
                )

# =====================================
# MEMBUAT JADWAL KOSONG
# =====================================

jadwal = buat_slot_jadwal()

# =====================================
# MAIN
# =====================================

if __name__=="__main__":

    print("="*60)
    print("SMART SCHEDULER V7")
    print("="*60)

    print()

    print("Jumlah Guru :",len(guru))

    print("Jumlah Kelas :",len(rombel))

    print("Jumlah Data Mengajar :",len(mengajar))

    print()

    print("Daftar Guru")

    print("----------------")

    for g in daftar_guru():

        print(g)

    print()

    print("Daftar Kelas")

    print("----------------")

    for k in daftar_kelas():

        print(k)

    print()

    print("Slot Jadwal berhasil dibuat.")

    print()

    print(jadwal.keys())
