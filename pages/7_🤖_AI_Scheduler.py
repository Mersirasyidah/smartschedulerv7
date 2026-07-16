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

def pembagian_jp(nilai):
    """
    Mengubah:
    2,2,1
    2,2
    3
    3.0
    menjadi list integer
    """

    import pandas as pd

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
            print("Pembagian tidak valid :", nilai)

    return hasil


# =====================================
# DATA MENGAJAR BERDASARKAN PRIORITAS
# =====================================

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
        by="Prioritas"
    )

    return data.reset_index(drop=True)


# =====================================
# CEK SLOT KOSONG
# =====================================

def slot_kosong(jadwal, kelas, hari, jam):

    return jadwal[kelas][hari][jam] is None


# =====================================
# CEK GURU SUDAH MENGAJAR
# =====================================

def guru_bentrok(jadwal, nama_guru, hari, jam):

    for kelas in jadwal:

        isi = jadwal[kelas][hari][jam]

        if isi is None:
            continue

        if isi["Guru"] == nama_guru:
            return True

    return False


# =====================================
# MENEMPATKAN SATU JP
# =====================================

def isi_slot(
    jadwal,
    kelas,
    hari,
    jam,
    guru_nama,
    mapel,
):

    jadwal[kelas][hari][jam] = {

        "Guru": guru_nama,

        "Mapel": mapel

    }


# =====================================
# MENCARI SLOT BERURUT
# =====================================

def cari_slot(
    jadwal,
    kelas,
    nama_guru,
    hari,
    panjang
):

    daftar = JAM[hari]

    for awal in daftar:

        akhir = awal + panjang - 1

        if akhir not in daftar:
            continue

        boleh = True

        for j in range(awal, akhir + 1):

            if not slot_kosong(
                jadwal,
                kelas,
                hari,
                j
            ):

                boleh = False

                break

            if guru_bentrok(
                jadwal,
                nama_guru,
                hari,
                j
            ):

                boleh = False

                break

        if boleh:

            return awal

    return None


# =====================================
# MENEMPATKAN SATU BLOK JP
# =====================================

def tempatkan_blok(
    jadwal,
    kelas,
    guru_id,
    guru_nama,
    mapel,
    panjang
):

    for hari in HARI:

        if hari == "Jumat" and panjang > 2:
            continue

        for jam in JAM[hari]:

            if not boleh_mengajar(
                guru_id,
                hari,
                jam
            ):
                continue

        awal = cari_slot(
            jadwal,
            kelas,
            guru_nama,
            hari,
            panjang
        )

        if awal is None:
            continue

        for j in range(
            awal,
            awal + panjang
        ):

            isi_slot(
                jadwal,
                kelas,
                hari,
                j,
                guru_nama,
                mapel
            )

        return True

    return False

# =====================================
# GENERATE JADWAL
# =====================================

def generate_jadwal():

    jadwal = buat_slot_jadwal()

    data = data_prioritas()

    gagal = []

    berhasil = 0

    for _, row in data.iterrows():

        guru_id = row["ID Guru"]

        guru_nama = row["Nama Guru"]

        mapel = row["Mapel"]

        kelas = row["Kelas"]

        jp = int(row["JP"])

        print(
    row["Nama Guru"],
    row["Mapel"],
    row["Kelas"],
    row["Pembagian"]
)

pembagian = pembagian_jp(row["Pembagian"])

        sukses = True

        # contoh :
        # 5 JP -> [2,2,1]

        for blok in pembagian:

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

            berhasil += 1

        else:

            gagal.append({

                "Guru": guru_nama,

                "Mapel": mapel,

                "Kelas": kelas,

                "JP": jp

            })

    return jadwal, gagal, berhasil


# =====================================
# UBAH JADWAL MENJADI DATAFRAME
# =====================================

def jadwal_dataframe(jadwal):

    rows = []

    for kelas in jadwal:

        for hari in HARI:

            for jam in JAM[hari]:

                isi = jadwal[kelas][hari][jam]

                if isi is None:

                    guru = ""

                    mapel = ""

                else:

                    guru = isi["Guru"]

                    mapel = isi["Mapel"]

                rows.append({

                    "Kelas": kelas,

                    "Hari": hari,

                    "Jam": jam,

                    "Guru": guru,

                    "Mapel": mapel

                })

    return pd.DataFrame(rows)


# =====================================
# RINGKASAN
# =====================================

def ringkasan(gagal, berhasil):

    print("=" * 60)

    print("HASIL GENERATE")

    print("=" * 60)

    print()

    print("Berhasil :", berhasil)

    print("Gagal :", len(gagal))

    print()

    if len(gagal):

        print("DATA YANG BELUM TERJADWAL")

        print()

        for g in gagal:

            print(

                g["Guru"],

                "-",

                g["Mapel"],

                "-",

                g["Kelas"]

            )


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    jadwal, gagal, berhasil = generate_jadwal()

    df = jadwal_dataframe(jadwal)

    print(df.head())

    print()

    ringkasan(gagal, berhasil)
