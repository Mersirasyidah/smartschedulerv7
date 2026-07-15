import streamlit as st
import pandas as pd
from database import load_database

st.set_page_config(
    page_title="Pemetaan Guru",
    page_icon="👨‍🏫",
    layout="wide"
)

db = load_database()

# -----------------------------
# Membaca sheet Guru
# -----------------------------
guru = db["Guru"]

st.title("📊 PEMETAAN GURU")

# =============================
# PILIH GURU
# =============================

daftar_guru = guru["Nama Guru"].sort_values().unique()

pilih_guru = st.selectbox(
    "Pilih Guru",
    daftar_guru
)

# =============================
# FILTER DATA
# =============================

data = guru[guru["Nama Guru"] == pilih_guru]

# =============================
# TAMPILKAN IDENTITAS
# =============================

st.subheader("Identitas Guru")

col1, col2 = st.columns(2)

with col1:

    st.write("**Nama Guru**")
    st.success(data.iloc[0]["Nama Guru"])

    st.write("**ID Guru**")
    st.info(data.iloc[0]["ID Guru"])

    st.write("**Hari MGMP**")
    st.warning(data.iloc[0]["Hari MGMP"])


with col2:

    st.write("**Prioritas**")
    st.info(data.iloc[0]["PRIORITAS"])

    st.write("**Jumlah JP / Kelas**")
    st.success(data.iloc[0]["JP"])


st.divider()

# =============================
# MATA PELAJARAN
# =============================

st.subheader("📖 Mata Pelajaran")

for m in data["Nama Mapel"]:

    st.write("✔", m)

st.divider()

# =============================
# KELAS
# =============================

st.subheader("🏫 Mengajar di Kelas")

kelas = []

for item in data["Kelas"]:

    kelas.extend(item.split(","))

kelas = sorted(kelas)

for k in kelas:

    st.write("✔", k)

st.divider()

# =============================
# RINGKASAN
# =============================

jumlah_kelas = len(kelas)

jp = int(data.iloc[0]["JP"])

total_jp = jumlah_kelas * jp

st.subheader("📈 Ringkasan")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Jumlah Kelas",
    jumlah_kelas
)

c2.metric(
    "JP per Kelas",
    jp
)

c3.metric(
    "Total Beban Mengajar",
    total_jp
)
