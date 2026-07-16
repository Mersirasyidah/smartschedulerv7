"""
=========================================================
SMART SCHEDULER V7
AI TIMETABLING ENGINE
Menggunakan Google OR-Tools CP-SAT Solver

BAGIAN 1
- Import Library
- Load Model
- Inisialisasi Solver
- Variabel Global
=========================================================
"""

# =====================================================
# IMPORT
# =====================================================

from ortools.sat.python import cp_model

import pandas as pd

from models import load_models

from config import HARI
from config import JAM
from config import MAX_JP_GURU

# =====================================================
# LOAD DATABASE MODEL
# =====================================================

model_data = load_models()

# =====================================================
# MEMBUAT SOLVER
# =====================================================

solver_model = cp_model.CpModel()

# =====================================================
# OBJECT SOLVER
# =====================================================

solver = cp_model.CpSolver()

# =====================================================
# VARIABEL KEPUTUSAN
# x[(guru,kelas,hari,jam,mapel)]
# =====================================================

x = {}

# =====================================================
# LIST GURU
# =====================================================

GURU = model_data.guru

# =====================================================
# LIST ROMBEL
# =====================================================

ROMBEL = model_data.rombel

# =====================================================
# LIST MENGAJAR
# =====================================================

MENGAJAR = model_data.mengajar

# =====================================================
# SLOT HARI
# =====================================================

HARI_LIST = HARI

# =====================================================
# SLOT JP
# =====================================================

JAM_LIST = JAM

# =====================================================
# MEMBUAT VARIABEL BOOLEAN
# =====================================================

def buat_variabel():

    print()

    print("="*60)

    print("MEMBUAT VARIABEL")

    print("="*60)

    jumlah = 0

    for item in MENGAJAR:

        for hari in HARI_LIST:

            for jam in JAM_LIST[hari]:

                key = (

                    item.id_guru,

                    item.kelas,

                    hari,

                    jam,

                    item.mapel

                )

                x[key] = solver_model.NewBoolVar(

                    f"{item.id_guru}_{item.kelas}_{hari}_{jam}_{item.mapel}"

                )

                jumlah += 1

    print()

    print("Jumlah Variable :", jumlah)

    return jumlah

# =====================================================
# INFO DATABASE
# =====================================================

def info():

    print()

    print("="*60)

    print("DATABASE")

    print("="*60)

    print()

    print("Guru :", len(GURU))

    print("Rombel :", len(ROMBEL))

    print("Mengajar :", len(MENGAJAR))

    print()

# =====================================================
# CEK ORTOOLS
# =====================================================

def test_solver():

    print()

    print("="*60)

    print("GOOGLE ORTOOLS")

    print("="*60)

    print()

    print(cp_model.__name__)

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    info()

    test_solver()

    buat_variabel()

# =====================================================
# BAGIAN 2
# CONSTRAINT DASAR
# =====================================================

print("\nMembangun Constraint Dasar...")

# =====================================================
# 1. SATU KELAS HANYA SATU MAPEL
# =====================================================

def constraint_kelas():

    print("Constraint : Satu kelas satu mapel")

    jumlah = 0

    for rombel in ROMBEL:

        kelas = rombel.nama

        for hari in HARI_LIST:

            for jam in JAM_LIST[hari]:

                variabel = []

                for item in MENGAJAR:

                    if item.kelas != kelas:
                        continue

                    key = (
                        item.id_guru,
                        item.kelas,
                        hari,
                        jam,
                        item.mapel
                    )

                    variabel.append(x[key])

                if len(variabel) > 0:

                    solver_model.Add(
                        sum(variabel) <= 1
                    )

                    jumlah += 1

    print("Constraint dibuat :", jumlah)


# =====================================================
# 2. GURU TIDAK BOLEH BENTROK
# =====================================================

def constraint_guru():

    print("Constraint : Guru tidak bentrok")

    jumlah = 0

    for guru in GURU:

        nama = guru.nama

        idguru = guru.id_guru

        for hari in HARI_LIST:

            for jam in JAM_LIST[hari]:

                variabel = []

                for item in MENGAJAR:

                    if item.id_guru != idguru:
                        continue

                    key = (
                        item.id_guru,
                        item.kelas,
                        hari,
                        jam,
                        item.mapel
                    )

                    variabel.append(x[key])

                if len(variabel) > 0:

                    solver_model.Add(
                        sum(variabel) <= 1
                    )

                    jumlah += 1

    print("Constraint dibuat :", jumlah)


# =====================================================
# 3. TOTAL JP SESUAI DATA
# =====================================================

def constraint_jumlah_jp():

    print("Constraint : Total JP")

    jumlah = 0

    for item in MENGAJAR:

        variabel = []

        for hari in HARI_LIST:

            for jam in JAM_LIST[hari]:

                key = (
                    item.id_guru,
                    item.kelas,
                    hari,
                    jam,
                    item.mapel
                )

                variabel.append(
                    x[key]
                )

        solver_model.Add(

            sum(variabel) == item.jp

        )

        jumlah += 1

    print("Constraint dibuat :", jumlah)


# =====================================================
# 4. MAKSIMAL JP GURU PER HARI
# =====================================================

def constraint_max_jp_guru():

    print("Constraint : Maksimal JP Guru")

    jumlah = 0

    for guru in GURU:

        for hari in HARI_LIST:

            variabel = []

            for item in MENGAJAR:

                if item.id_guru != guru.id_guru:
                    continue

                for jam in JAM_LIST[hari]:

                    key = (
                        item.id_guru,
                        item.kelas,
                        hari,
                        jam,
                        item.mapel
                    )

                    variabel.append(x[key])

            if len(variabel) > 0:

                solver_model.Add(

                    sum(variabel) <= MAX_JP_GURU

                )

                jumlah += 1

    print("Constraint dibuat :", jumlah)


# =====================================================
# MEMBANGUN SEMUA CONSTRAINT DASAR
# =====================================================

def build_constraint():

    print()

    print("=" * 60)
    print("MEMBANGUN CONSTRAINT")
    print("=" * 60)

    constraint_kelas()

    constraint_guru()

    constraint_jumlah_jp()

    constraint_max_jp_guru()

    print()

    print("Constraint dasar selesai.")


