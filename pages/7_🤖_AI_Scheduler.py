import streamlit as st
import pandas as pd

from database import load_database
from scheduler import Scheduler


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
# Ambil Data Database
# =====================================

guru = db["Guru"]

mengajar = db["Guru_Mengajar"]

rombel = db["Rombel"]



# =====================================
# Statistik
# =====================================

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


    st.info(
        "Menyiapkan AI Scheduler..."
    )


    # ==============================
    # Konversi Database
    # ==============================


    try:


        # Data guru

        data_guru = (
            guru["nama_guru"]
            .tolist()
        )


        # Data kelas

        data_kelas = (
            rombel["kelas"]
            .tolist()
        )


        # Mata pelajaran

        data_mapel = (
            mengajar["mapel"]
            .unique()
            .tolist()
        )



        # Beban mengajar

        data_jadwal = pd.DataFrame({

            "guru":
                mengajar["nama_guru"],


            "kelas":
                mengajar["kelas"],


            "mapel":
                mengajar["mapel"],


            "jam":
                mengajar["jam"]

        })



    except Exception as e:


        st.error(
            "Format database belum sesuai"
        )


        st.exception(e)

        st.stop()



    # ==============================
    # Membuat Scheduler Engine
    # ==============================


    scheduler = Scheduler(

        data_guru,

        data_kelas,

        data_mapel,

        data_jadwal

    )



    st.write(
        "Data Scheduler siap:"
    )


    st.write(
        f"Guru : {len(data_guru)}"
    )


    st.write(
        f"Kelas : {len(data_kelas)}"
    )


    st.write(
        f"Mapel : {len(data_mapel)}"
    )



    # ==============================
    # Generate Index
    # ==============================


    scheduler.create_index()



    st.success(
        "Index jadwal berhasil dibuat"
    )



    # ==============================
    # Membuat Variabel AI
    # ==============================


    scheduler.create_variables()



    st.success(
        "Variabel AI berhasil dibuat"
    )



    # ==============================
    # Pasang Constraint
    # ==============================


    if hasattr(
        scheduler,
        "build_constraints"
    ):


        scheduler.build_constraints()


        st.success(
            "Constraint berhasil dipasang"
        )


    else:


        st.warning(
            """
            Engine constraint belum tersedia.
            Pastikan scheduler.py sudah menggunakan
            Bagian 2.
            """
        )



    st.success(
        "🤖 AI Scheduler Engine siap dijalankan"
    )
