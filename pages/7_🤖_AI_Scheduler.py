import streamlit as st
import pandas as pd

from database import load_database
from scheduler import Scheduler


# ==========================================================
# KONFIGURASI HALAMAN
# ==========================================================

st.set_page_config(

    page_title="AI Scheduler",

    page_icon="🤖",

    layout="wide"

)


st.title("🤖 AI Scheduler V2")

st.caption(
    "Smart Scheduler V2 - AI Timetable Generator"
)

st.divider()


# ==========================================================
# LOAD DATABASE
# ==========================================================

try:

    db = load_database()

except Exception as e:

    st.error("Database gagal dibaca.")

    st.exception(e)

    st.stop()


# ==========================================================
# MEMBACA TABEL
# ==========================================================

required_tables = [

    "Guru",

    "Guru_Mengajar",

    "Rombel",

    "Mapel",

    "Hari_Jam"

]

missing = [

    table

    for table in required_tables

    if table not in db

]

if missing:

    st.error(
        f"Tabel berikut belum tersedia : {', '.join(missing)}"
    )

    st.stop()


guru = db["Guru"]

mengajar = db["Guru_Mengajar"]

rombel = db["Rombel"]

mapel = db["Mapel"]

hari_jam = db["Hari_Jam"]


# ==========================================================
# DASHBOARD
# ==========================================================

st.subheader("📊 Statistik Database")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(

    "Guru",

    len(guru)

)

c2.metric(

    "Mapel",

    len(mapel)

)

c3.metric(

    "Rombel",

    len(rombel)

)

c4.metric(

    "Mengajar",

    len(mengajar)

)

c5.metric(

    "Hari/Jam",

    len(hari_jam)

)

st.divider()


# ==========================================================
# PREVIEW DATABASE
# ==========================================================

with st.expander("📂 Preview Database"):

    tab1, tab2, tab3, tab4, tab5 = st.tabs(

        [

            "Guru",

            "Guru Mengajar",

            "Rombel",

            "Mapel",

            "Hari_Jam"

        ]

    )

    with tab1:

        st.dataframe(

            guru,

            use_container_width=True

        )

    with tab2:

        st.dataframe(

            mengajar,

            use_container_width=True

        )

    with tab3:

        st.dataframe(

            rombel,

            use_container_width=True

        )

    with tab4:

        st.dataframe(

            mapel,

            use_container_width=True

        )

    with tab5:

        st.dataframe(

            hari_jam,

            use_container_width=True

        )

st.divider()


# ==========================================================
# SESSION STATE
# ==========================================================

if "jadwal" not in st.session_state:

    st.session_state.jadwal = pd.DataFrame()

if "scheduler" not in st.session_state:

    st.session_state.scheduler = None


# ==========================================================
# TOMBOL GENERATE
# ==========================================================

generate = st.button(

    "🚀 Generate Jadwal",

    use_container_width=True,

    type="primary"

)

# ==========================================================
# GENERATE SCHEDULER
# ==========================================================

if generate:

    st.divider()

    st.subheader("🤖 AI Scheduler")

    progress = st.progress(0)

    status = st.empty()

    try:

        # -----------------------------------------------
        # Membuat Scheduler Engine
        # -----------------------------------------------

        status.info("Membuat Scheduler Engine...")

        scheduler = Scheduler(db)

        st.session_state.scheduler = scheduler

        progress.progress(10)

        st.success("✅ Scheduler Engine berhasil dibuat")


        # -----------------------------------------------
        # Persiapan Engine
        # -----------------------------------------------

        status.info("Menyiapkan database...")

        scheduler.prepare()

        progress.progress(25)

        st.success("✅ Database berhasil diproses")


        # -----------------------------------------------
        # Membuat Index
        # -----------------------------------------------

        status.info("Membuat index jadwal...")

        scheduler.create_index()

        progress.progress(45)

        st.success("✅ Index berhasil dibuat")


        # -----------------------------------------------
        # Variable AI
        # -----------------------------------------------

        status.info("Membuat Variable AI...")

        scheduler.create_variables()

        progress.progress(60)

        st.success("✅ Variable AI berhasil dibuat")


        # -----------------------------------------------
        # Constraint
        # -----------------------------------------------

        status.info("Memasang Constraint...")

        scheduler.build_constraints()

        progress.progress(80)

        st.success("✅ Constraint berhasil dipasang")


        # -----------------------------------------------
        # Solver
        # -----------------------------------------------

        status.info("Menjalankan AI Solver...")

        hasil = scheduler.solve()

        progress.progress(95)


        # -----------------------------------------------
        # Hasil
        # -----------------------------------------------

        if hasil:

            jadwal = scheduler.to_dataframe()

            st.session_state.jadwal = jadwal

            progress.progress(100)

            status.success("AI berhasil membuat jadwal.")

            st.success("🎉 Jadwal berhasil dibuat")

        else:

            status.error("AI tidak menemukan solusi.")

            st.error(
                """
                Penyebab yang mungkin:

                • JP melebihi slot

                • Guru bentrok

                • Kelas bentrok

                • Constraint terlalu ketat
                """
            )

    except Exception as e:

        st.error("Terjadi error saat Generate Jadwal")

        st.exception(e)

