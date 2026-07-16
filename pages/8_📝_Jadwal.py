import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Jadwal",
    page_icon="📅",
    layout="wide"
)



st.title(
    "📅 Jadwal Pelajaran"
)


st.caption(
    "Smart Scheduler V7"
)



# ===============================
# AMBIL DATA
# ===============================


if "jadwal" in st.session_state:


    jadwal = st.session_state["jadwal"]


else:


    try:

        jadwal = pd.read_csv(
            "hasil_jadwal.csv"
        )


    except:


        st.warning(
            """
            Jadwal belum tersedia.

            Silakan Generate Jadwal terlebih dahulu.
            """
        )

        st.stop()



# ===============================
# TAMPILKAN
# ===============================


st.success(
    "Jadwal ditemukan"
)



st.dataframe(

    jadwal,

    use_container_width=True,

    hide_index=True

)



st.divider()



# ===============================
# FILTER KELAS
# ===============================


st.subheader(
    "🏫 Jadwal Per Kelas"
)



kelas = st.selectbox(

    "Pilih Kelas",

    jadwal["Kelas"].unique()

)



st.dataframe(

    jadwal[
        jadwal["Kelas"]==kelas
    ],

    use_container_width=True,

    hide_index=True

)



st.divider()



# ===============================
# FILTER GURU
# ===============================


st.subheader(
    "👨‍🏫 Jadwal Per Guru"
)



guru = st.selectbox(

    "Pilih Guru",

    jadwal["Guru"].unique()

)



st.dataframe(

    jadwal[
        jadwal["Guru"]==guru
    ],

    use_container_width=True,

    hide_index=True

)
