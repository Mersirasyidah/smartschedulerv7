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

from scheduler import Scheduler
import pandas as pd


if st.button("🚀 Generate Jadwal"):


    st.info(
        "Menyiapkan AI Scheduler..."
    )


    # ==========================
    # DATA SEMENTARA
    # nanti diganti database
    # ==========================


    data_guru = [
        "Budi",
        "Siti",
        "Andi"
    ]


    data_kelas = [
        "7A",
        "7B",
        "8A"
    ]


    data_mapel = [
        "Matematika",
        "Informatika",
        "IPA"
    ]



    data_jadwal = pd.DataFrame({

        "guru":[
            "Budi",
            "Siti",
            "Andi"
        ],

        "kelas":[
            "7A",
            "7B",
            "8A"
        ],

        "mapel":[
            "Matematika",
            "Informatika",
            "IPA"
        ],

        "jam":[
            5,
            3,
            4
        ]

    })



    # Membuat engine

    scheduler = Scheduler(

        data_guru,
        data_kelas,
        data_mapel,
        data_jadwal

    )



    # membuat kemungkinan jadwal

    scheduler.create_index()



    # membuat variabel AI

    scheduler.create_variables()



    # pasang aturan

    scheduler.build_constraints()



    st.success(
        "Engine Scheduler berhasil dibuat"
    )
