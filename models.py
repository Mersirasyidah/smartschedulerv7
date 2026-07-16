"""
=========================================================
SMART SCHEDULER V7
MODELS.PY

Bagian 1
- Import Library
- Data Model
- Dataclass
=========================================================
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ==========================================================
# MODEL GURU
# ==========================================================

@dataclass
class Guru:

    id_guru: str

    nama: str

    mgmp: str

    prioritas: int

    mapel: List[str] = field(default_factory=list)

    kelas: List[str] = field(default_factory=list)

    jp_total: int = 0

    def __str__(self):

        return f"{self.id_guru} - {self.nama}"

# ==========================================================
# MODEL MATA PELAJARAN
# ==========================================================

@dataclass
class Mapel:

    kode: str

    nama: str

    kelompok: str = ""

    def __str__(self):

        return self.nama

# ==========================================================
# MODEL ROMBEL
# ==========================================================

@dataclass
class Rombel:

    nama: str

    tingkat: int

    wali_kelas: str = ""

    def __str__(self):

        return self.nama

# ==========================================================
# MODEL HARI
# ==========================================================

@dataclass
class Hari:

    nama: str

    jumlah_jp: int

    durasi_jp: int

    def __str__(self):

        return self.nama

# ==========================================================
# MODEL SLOT WAKTU
# ==========================================================

@dataclass
class SlotJam:

    hari: str

    jam_ke: int

    mulai: str

    selesai: str

    aktif: bool = True

    def __str__(self):

        return f"{self.hari} JP {self.jam_ke}"

# ==========================================================
# MODEL MENGAJAR
# (masih kosong, akan diisi pada Bagian 2)
# ==========================================================

@dataclass
class Mengajar:

    id_guru: str

    guru: str

    mapel: str

    kelas: str

    jp: int

    pembagian: List[int]

# ==========================================================
# MODEL PENEMPATAN
# ==========================================================

@dataclass
class Penempatan:

    kelas: str

    hari: str

    jam: int

    guru: str

    mapel: str

    id_guru: str

# ==========================================================
# MODEL HASIL JADWAL
# ==========================================================

@dataclass
class Jadwal:

    data: Dict = field(default_factory=dict)

    def tambah(
        self,
        kelas,
        hari,
        jam,
        guru,
        mapel,
        id_guru
    ):

        if kelas not in self.data:

            self.data[kelas] = {}

        if hari not in self.data[kelas]:

            self.data[kelas][hari] = {}

        self.data[kelas][hari][jam] = Penempatan(

            kelas=kelas,

            hari=hari,

            jam=jam,

            guru=guru,

            mapel=mapel,

            id_guru=id_guru

        )

    def kosong(
        self,
        kelas,
        hari,
        jam
    ):

        if kelas not in self.data:

            return True

        if hari not in self.data[kelas]:

            return True

        return jam not in self.data[kelas][hari]

    def ambil(
        self,
        kelas,
        hari,
        jam
    ):

        if self.kosong(kelas, hari, jam):

            return None

        return self.data[kelas][hari][jam]

# ==========================================================
# DATABASE OBJECT
# ==========================================================

@dataclass
class DatabaseModel:

    guru: List[Guru] = field(default_factory=list)

    mapel: List[Mapel] = field(default_factory=list)

    rombel: List[Rombel] = field(default_factory=list)

    hari: List[Hari] = field(default_factory=list)

    slot: List[SlotJam] = field(default_factory=list)

    mengajar: List[Mengajar] = field(default_factory=list)

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("="*50)

    print("SMART SCHEDULER V7")

    print("MODELS")

    print("="*50)

    guru = Guru(

        id_guru="G01",

        nama="Purwanto",

        mgmp="Jumat",

        prioritas=1

    )

    print(guru)

    rombel = Rombel(

        nama="7A",

        tingkat=7

    )

    print(rombel)

  """
=========================================================
MODELS.PY
Bagian 2
Parser dan Loader Data
=========================================================
"""

import pandas as pd
from database import load_database


# ==========================================================
# LOAD DATABASE EXCEL
# ==========================================================

db = load_database()


# ==========================================================
# PARSER PEMBAGIAN JP
# Contoh:
# "2,2,1" -> [2,2,1]
# ==========================================================

def parse_pembagian(teks):

    if pd.isna(teks):
        return []

    teks = str(teks).strip()

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

            print("Pembagian salah :", teks)

    return hasil


# ==========================================================
# PARSER DAFTAR KELAS
# "7A,7B,7C"
# ==========================================================

def parse_kelas(teks):

    if pd.isna(teks):
        return []

    teks = str(teks).strip()

    if teks == "":
        return []

    hasil = []

    for x in teks.split(","):

        x = x.strip()

        if x != "":
            hasil.append(x)

    return hasil


# ==========================================================
# PARSER MAPEL
# "Prakarya, Bahasa Jawa"
# ==========================================================

def parse_mapel(teks):

    if pd.isna(teks):
        return []

    teks = str(teks).strip()

    hasil = []

    for x in teks.split(","):

        x = x.strip()

        if x != "":
            hasil.append(x)

    return hasil


# ==========================================================
# LOAD GURU
# ==========================================================

def load_guru():

    data = db["Guru"]

    hasil = []

    for _, row in data.iterrows():

        g = Guru(

            id_guru=str(row["ID Guru"]),

            nama=row["Nama Guru"],

            mgmp=row["Hari MGMP"],

            prioritas=int(row["Prioritas"])

        )

        hasil.append(g)

    return hasil


# ==========================================================
# LOAD ROMBEL
# ==========================================================

def load_rombel():

    data = db["Rombel"]

    hasil = []

    for _, row in data.iterrows():

        tingkat = int(str(row["Kelas"])[0])

        hasil.append(

            Rombel(

                nama=row["Kelas"],

                tingkat=tingkat

            )

        )

    return hasil


# ==========================================================
# LOAD HARI
# ==========================================================

def load_hari():

    hasil = []

    hasil.append(Hari("Senin",9,40))
    hasil.append(Hari("Selasa",9,40))
    hasil.append(Hari("Rabu",9,40))
    hasil.append(Hari("Kamis",9,40))
    hasil.append(Hari("Jumat",6,30))

    return hasil


# ==========================================================
# LOAD SLOT JAM
# ==========================================================

def load_slot():

    data = db["Hari_Jam"]

    hasil = []

    for _, row in data.iterrows():

        hasil.append(

            SlotJam(

                hari=row["Hari"],

                jam_ke=int(row["JP"]),

                mulai=row["Mulai"],

                selesai=row["Selesai"],

                aktif=True

            )

        )

    return hasil


# ==========================================================
# LOAD GURU MENGAJAR
# ==========================================================

def load_mengajar():

    data = db["Guru_Mengajar"]

    hasil = []

    for _, row in data.iterrows():

        daftar_kelas = parse_kelas(row["Kelas"])

        daftar_mapel = parse_mapel(row["Mapel"])

        pembagian = parse_pembagian(row["Pembagian"])

        for mapel in daftar_mapel:

            for kelas in daftar_kelas:

                hasil.append(

                    Mengajar(

                        id_guru=row["ID Guru"],

                        guru=row["Nama Guru"],

                        mapel=mapel,

                        kelas=kelas,

                        jp=int(row["JP"]),

                        pembagian=pembagian

                    )

                )

    return hasil

"""
=========================================================
MODELS.PY
Bagian 3
DatabaseModel Loader
=========================================================
"""

# ==========================================================
# MEMBANGUN DATABASE MODEL
# ==========================================================

def load_models():

    model = DatabaseModel()

    print("=" * 60)
    print("MEMBACA DATABASE")
    print("=" * 60)

    # ---------------------------------
    # Guru
    # ---------------------------------

    print("Loading Guru...")

    model.guru = load_guru()

    print("   ", len(model.guru), "Guru")

    # ---------------------------------
    # Rombel
    # ---------------------------------

    print("Loading Rombel...")

    model.rombel = load_rombel()

    print("   ", len(model.rombel), "Rombel")

    # ---------------------------------
    # Hari
    # ---------------------------------

    print("Loading Hari...")

    model.hari = load_hari()

    print("   ", len(model.hari), "Hari")

    # ---------------------------------
    # Slot
    # ---------------------------------

    print("Loading Slot...")

    model.slot = load_slot()

    print("   ", len(model.slot), "Slot")

    # ---------------------------------
    # Mengajar
    # ---------------------------------

    print("Loading Guru Mengajar...")

    model.mengajar = load_mengajar()

    print("   ", len(model.mengajar), "Data Mengajar")

    return model


# ==========================================================
# VALIDASI DATABASE
# ==========================================================

def validasi(model):

    print()
    print("=" * 60)
    print("VALIDASI")
    print("=" * 60)

    error = 0

    # ---------------------------------
    # Guru tanpa MGMP
    # ---------------------------------

    for g in model.guru:

        if g.mgmp is None:

            print("MGMP kosong :", g.nama)

            error += 1

        elif str(g.mgmp).strip() == "":

            print("MGMP kosong :", g.nama)

            error += 1

    # ---------------------------------
    # JP tidak sesuai
    # ---------------------------------

    for m in model.mengajar:

        if sum(m.pembagian) != m.jp:

            print()

            print("Pembagian JP salah")

            print(m.guru)

            print(m.mapel)

            print(m.kelas)

            print("JP :", m.jp)

            print("Pembagian :", m.pembagian)

            error += 1

    print()

    if error == 0:

        print("VALIDASI BERHASIL")

    else:

        print("Jumlah Error :", error)

    return error


# ==========================================================
# RINGKASAN DATABASE
# ==========================================================

def info(model):

    print()

    print("=" * 60)

    print("DATABASE")

    print("=" * 60)

    print()

    print("Guru :", len(model.guru))

    print("Mengajar :", len(model.mengajar))

    print("Rombel :", len(model.rombel))

    print("Hari :", len(model.hari))

    print("Slot :", len(model.slot))


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    model = load_models()

    info(model)

    validasi(model)

    print()

    print("Contoh Guru")

    print(model.guru[0])

    print()

    print("Contoh Mengajar")

    print(model.mengajar[0])

