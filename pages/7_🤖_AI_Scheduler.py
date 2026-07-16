import pandas as pd
import random
from database import load_database

# =====================================================
# LOAD DATABASE
# =====================================================

db = load_database()

guru = db["Guru"]
mengajar = db["Guru_Mengajar"]
rombel = db["Rombel"]
hari_jam = db["Hari_Jam"]

# =====================================================
# HARI BELAJAR
# =====================================================

HARI = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat"
]

# =====================================================
# SLOT JP
# =====================================================

JAM = {
    "Senin":  [1,2,3,4,5,6,7,8,9],
    "Selasa": [1,2,3,4,5,6,7,8,9],
    "Rabu":   [1,2,3,4,5,6,7,8,9],
    "Kamis":  [1,2,3,4,5,6,7,8,9],
    "Jumat":  [1,2,3,4,5,6]
}

# =====================================================
# MEMBUAT SLOT JADWAL
# =====================================================

def buat_slot_jadwal():

    jadwal = {}

    daftar = sorted(rombel["Kelas"].unique())

    for kelas in daftar:

        jadwal[kelas] = {}

        for hari in HARI:

            jadwal[kelas][hari] = {}

            for jam in JAM[hari]:

                jadwal[kelas][hari][jam] = None

    return jadwal


# =====================================================
# PEMBAGIAN JP
# =====================================================

def pembagian_jp(nilai):

    """
    Contoh:

    2,2,1

    menjadi

    [2,2,1]
    """

    if pd.isna(nilai):

        return []

    teks = str(nilai).strip()

    if teks == "":

        return []

    hasil = []

    for x in teks.split(","):

        x = x.strip()

        if x == "":

            continue

        try:

            hasil.append(int(float(x)))

        except Exception:

            print("Pembagian salah :", nilai)

            return []

    return hasil


# =====================================================
# HARI MGMP
# =====================================================

def hari_mgmp(id_guru):

    data = guru[
        guru["ID Guru"] == id_guru
    ]

    if len(data) == 0:

        return None

    return data.iloc[0]["Hari MGMP"]


# =====================================================
# PRIORITAS
# =====================================================

def prioritas(id_guru):

    data = guru[
        guru["ID Guru"] == id_guru
    ]

    if len(data) == 0:

        return 3

    return int(data.iloc[0]["Prioritas"])


# =====================================================
# BOLEH MENGAJAR
# =====================================================

def boleh_mengajar(id_guru, hari, jam):

    mgmp = hari_mgmp(id_guru)

    if mgmp == hari:

        if jam >= 5:

            return False

    return True


# =====================================================
# DATA PRIORITAS
# =====================================================

def data_prioritas():

    data = mengajar.merge(

        guru[
            [
                "ID Guru",
                "Hari MGMP",
                "Prioritas"
            ]
        ],

        on="ID Guru"

    )

    data = data.sort_values(

        by=[
            "Prioritas",
            "Nama Guru",
            "Kelas"
        ]

    )

    return data.reset_index(drop=True)


# =====================================================
# MENAMPILKAN DATABASE
# =====================================================

def info_database():

    print("=" * 60)

    print("SMART SCHEDULER V7")

    print("=" * 60)

    print()

    print("Jumlah Guru :", len(guru))

    print("Jumlah Mengajar :", len(mengajar))

    print("Jumlah Kelas :", len(rombel))

    print()

    print("Hari Belajar")

    print(HARI)

    print()

    print("Total Slot")

    total = 0

    for h in HARI:

        total += len(JAM[h])

    print(total)

    print()


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    info_database()

    jadwal = buat_slot_jadwal()

    print("Slot berhasil dibuat")

    print()

    print(jadwal.keys())

# =====================================================
# CEK SLOT KOSONG
# =====================================================

def slot_kosong(jadwal, kelas, hari, jam):
    return jadwal[kelas][hari][jam] is None


# =====================================================
# CEK GURU BENTROK
# =====================================================

def guru_bentrok(jadwal, guru_nama, hari, jam):

    for kls in jadwal.keys():

        data = jadwal[kls][hari][jam]

        if data is None:
            continue

        if data["Guru"] == guru_nama:
            return True

    return False


# =====================================================
# CEK KELAS BENTROK
# =====================================================

def kelas_bentrok(jadwal, kelas, hari, jam):

    return jadwal[kelas][hari][jam] is not None


# =====================================================
# HIT

# =====================================================
# GENERATE JADWAL
# =====================================================

def generate_jadwal():

    jadwal = buat_slot_jadwal()

    data = data_prioritas()

    berhasil = []
    gagal = []

    print("=" * 60)
    print("GENERATE JADWAL")
    print("=" * 60)

    for _, row in data.iterrows():

        guru_id = row["ID Guru"]
        guru_nama = row["Nama Guru"]
        mapel = row["Mapel"]
        kelas = row["Kelas"]

        jp = int(row["JP"])

        blok_jp = pembagian_jp(row["Pembagian"])

        if len(blok_jp) == 0:

            gagal.append({
                "Guru": guru_nama,
                "Mapel": mapel,
                "Kelas": kelas,
                "Alasan": "Pembagian JP tidak valid"
            })

            continue

        sukses = True

        for blok in blok_jp:

            hasil = tempatkan_blok(
                jadwal,
                kelas,
                guru_id,
                guru_nama,
                mapel,
                blok
            )

            if not hasil:

                sukses = False

                break

        if sukses:

            berhasil.append({
                "Guru": guru_nama,
                "Mapel": mapel,
                "Kelas": kelas
            })

        else:

            gagal.append({
                "Guru": guru_nama,
                "Mapel": mapel,
                "Kelas": kelas,
                "Alasan": "Tidak menemukan slot"
            })

    return jadwal, berhasil, gagal


# =====================================================
# JADWAL → DATAFRAME
# =====================================================

def jadwal_to_dataframe(jadwal):

    hasil = []

    for kelas in jadwal.keys():

        for hari in HARI:

            for jam in JAM[hari]:

                isi = jadwal[kelas][hari][jam]

                if isi is None:

                    hasil.append({
                        "Kelas": kelas,
                        "Hari": hari,
                        "Jam": jam,
                        "Guru": "",
                        "Mapel": ""
                    })

                else:

                    hasil.append({
                        "Kelas": kelas,
                        "Hari": hari,
                        "Jam": jam,
                        "Guru": isi["Guru"],
                        "Mapel": isi["Mapel"]
                    })

    return pd.DataFrame(hasil)


# =====================================================
# SIMPAN KE EXCEL
# =====================================================

def simpan_excel(df):

    file = "hasil_jadwal.xlsx"

    with pd.ExcelWriter(
        file,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Jadwal",
            index=False
        )

    return file


# =====================================================
# RINGKASAN
# =====================================================

def ringkasan(berhasil, gagal):

    print()

    print("=" * 60)

    print("HASIL GENERATE")

    print("=" * 60)

    print()

    print("Berhasil :", len(berhasil))

    print("Gagal :", len(gagal))

    if len(gagal):

        print()

        print("Belum Terjadwal")

        for g in gagal:

            print(
                g["Guru"],
                "-",
                g["Mapel"],
                "-",
                g["Kelas"],
                "-",
                g["Alasan"]
            )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    info_database()

    jadwal, berhasil, gagal = generate_jadwal()

    df = jadwal_to_dataframe(jadwal)

    print(df.head())

    ringkasan(berhasil, gagal)

    simpan_excel(df)

    print()

    print("File hasil_jadwal.xlsx berhasil dibuat.")
