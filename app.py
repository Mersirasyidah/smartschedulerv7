import streamlit as st
from database import load_database

# Konfigurasi halaman
st.set_page_config(
    page_title="Smart Scheduler V7",
    page_icon="📚",
    layout="wide"
)

# Membaca database
db = load_database()

# Judul
st.title("📚 SMART SCHEDULER V7")
st.subheader("Sistem Penyusunan Jadwal Pembelajaran SMP")

st.divider()

# Menampilkan nama sheet
st.header("📂 Database")

st.write("Sheet yang berhasil dibaca:")

for sheet in db.keys():
    st.success(sheet)

st.divider()

# Statistik Dashboard
st.header("📊 Dashboard")

col1, col2, col3 = st.columns(3)

# Jumlah guru
if "Guru" in db:
    jumlah_guru = len(db["Guru"])
else:
    jumlah_guru = 0

# Jumlah mapel
if "Mapel" in db:
    jumlah_mapel = len(db["Mapel"])
else:
    jumlah_mapel = 0

# Jumlah rombel
if "Rombel" in db:
    jumlah_rombel = len(db["Rombel"])
else:
    jumlah_rombel = 0

col1.metric("👨‍🏫 Guru", jumlah_guru)
col2.metric("📖 Mata Pelajaran", jumlah_mapel)
col3.metric("🏫 Rombel", jumlah_rombel)

st.divider()

# Preview Data Guru
if "Guru" in db:

    st.subheader("Preview Data Guru")

    st.dataframe(db["Guru"], use_container_width=True)
