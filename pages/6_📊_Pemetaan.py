import streamlit as st
import pandas as pd
from database import load_database

st.set_page_config(
    page_title="Pemetaan Guru",
    page_icon="📊",
    layout="wide"
)

st.title("📊 PEMETAAN GURU")

# ==========================
# Load Database
# ==========================

db = load_database()

guru = db["Guru"]
mengajar = db["Guru_Mengajar"]

# ==========================
# Pilih Guru
# ==========================

nama_guru = sorted(guru["Nama Guru"].unique())

pilih = st.selectbox(
    "Pilih Guru",
    nama_guru
)

# ==========================
# Data Guru
# ==========================

data_guru = guru[guru["Nama Guru"] == pilih]

if data_guru.empty:
    st.warning("Guru tidak ditemukan.")
    st.stop()

info = data_guru.iloc[0]

# ==========================
# Data Mengajar
# ==========================

data_mengajar = mengajar[
    mengajar["ID Guru"] == info["ID Guru"]
]

# ==========================
# Identitas
# ==========================

st.subheader("👨‍🏫 Identitas Guru")

c1, c2 = st.columns(2)

with c1:

    st.info(f"**ID Guru :** {info['ID Guru']}")
    st.info(f"**Nama Guru :** {info['Nama Guru']}")
    st.info(f"**Status :** {info['Status']}")

with c2:

    st.info(f"**Hari MGMP :** {info['Hari MGMP']}")
    st.info(f"**Prioritas :** {info['Prioritas']}")

st.divider()

# ==========================
# Mengajar
# ==========================

st.subheader("📖 Mata Pelajaran yang Diampu")

if data_mengajar.empty:

    st.warning("Belum ada data mengajar.")

else:

    st.dataframe(
        data_mengajar,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================
# Ringkasan
# ==========================

if not data_mengajar.empty:

    jumlah_kelas = len(data_mengajar)

    total_jp = data_mengajar["JP"].sum()

    jumlah_mapel = data_mengajar["Mapel"].nunique()

    st.subheader("📈 Ringkasan Beban Mengajar")

    a, b, c = st.columns(3)

    a.metric(
        "Jumlah Kelas",
        jumlah_kelas
    )

    b.metric(
        "Jumlah Mapel",
        jumlah_mapel
    )

    c.metric(
        "Total JP",
        total_jp
    )

st.divider()

# ==========================
# Daftar Kelas
# ==========================

if not data_mengajar.empty:

    st.subheader("🏫 Daftar Kelas")

    kelas = sorted(data_mengajar["Kelas"].tolist())

    for k in kelas:
        st.write("✅", k)

st.divider()

# ==========================
# Grafik
# ==========================

if not data_mengajar.empty:

    st.subheader("📊 Distribusi JP")

    chart = (
        data_mengajar
        .groupby("Mapel")["JP"]
        .sum()
    )

    st.bar_chart(chart)
