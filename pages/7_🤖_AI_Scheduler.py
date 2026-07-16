import streamlit as st
from database import load_database

# =====================================
# Konfigurasi Halaman
# =====================================

st.set_page_config(
    page_title="AI Scheduler",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Scheduler")
st.caption("Smart Scheduler V7")

# =====================================
# Load Database
# =====================================

try:

    db = load_database()

except Exception as e:

    st.error("Database gagal dibaca")

    st.exception(e)

    st.stop()

# =====================================
# Statistik
# =====================================

guru = db["Guru"]
mengajar = db["Guru_Mengajar"]
rombel = db["Rombel"]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Guru",
    len(guru)
)

col2.metric(
    "Mengajar",
    len(mengajar)
)

col3.metric(
    "Rombel",
    len(rombel)
)

st.divider()

# =====================================
# Tombol Generate
# =====================================

if st.button("🚀 Generate Jadwal"):

    progress = st.progress(0)

    for i in range(100):

        progress.progress(i + 1)

    st.success("Engine Scheduler belum dibuat.")

    st.info(
        "Tahap berikutnya kita akan menghubungkan scheduler.py."
    )

st.divider()

# =====================================
# Preview Data Mengajar
# =====================================

st.subheader("Preview Data Guru Mengajar")

st.dataframe(
    mengajar,
    use_container_width=True
)

st.divider()

st.subheader("Preview Guru")

st.dataframe(
    guru,
    use_container_width=True
)
