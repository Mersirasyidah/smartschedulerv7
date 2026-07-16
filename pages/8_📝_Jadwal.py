import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Jadwal Pelajaran",
    page_icon="📅",
    layout="wide"
)


st.title("📅 Jadwal Pelajaran")

st.caption(
    "Smart Scheduler V7"
)



# =====================================
# Membaca hasil jadwal
# =====================================

try:

    jadwal = pd.read_csv(
        "hasil_jadwal.csv"
    )


except:


    st.warning(
        """
        Jadwal belum tersedia.

        Silakan Generate Jadwal
        terlebih dahulu.
        """
    )

    st.stop()



# =====================================
# Tampilan
# =====================================


tab1, tab2, tab3 = st.tabs(
    [
        "📋 Semua Jadwal",
        "👨‍🏫 Per Guru",
        "🏫 Per Kelas"
    ]
)



# =====================================
# Semua Jadwal
# =====================================


with tab1:


    st.dataframe(

        jadwal,

        use_container_width=True

    )



# =====================================
# Guru
# =====================================


with tab2:


    guru = st.selectbox(

        "Pilih Guru",

        jadwal["Guru"].unique()

    )


    hasil = jadwal[
        jadwal["Guru"] == guru
    ]


    st.dataframe(
        hasil,
        use_container_width=True
    )



# =====================================
# Kelas
# =====================================


with tab3:


    kelas = st.selectbox(

        "Pilih Kelas",

        jadwal["Kelas"].unique()

    )


    hasil = jadwal[
        jadwal["Kelas"] == kelas
    ]


    st.dataframe(
        hasil,
        use_container_width=True
    )
