import streamlit as st


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



# =====================================
# CEK HASIL GENERATE
# =====================================


if "jadwal" not in st.session_state:


    st.warning(
        """
        Jadwal belum tersedia.

        Silakan masuk ke menu:
        🤖 AI Scheduler

        kemudian klik:
        🚀 Generate Jadwal
        """
    )


    st.stop()



jadwal = st.session_state["jadwal"]



# =====================================
# TAMPILKAN SEMUA
# =====================================


st.subheader(
    "📋 Semua Jadwal"
)


st.dataframe(

    jadwal,

    use_container_width=True,

    hide_index=True

)



st.divider()



# =====================================
# PER KELAS
# =====================================


st.subheader(
    "🏫 Jadwal Per Kelas"
)


kelas = st.selectbox(

    "Pilih Kelas",

    jadwal["Kelas"].unique()

)



st.dataframe(

    jadwal[
        jadwal["Kelas"] == kelas
    ],

    use_container_width=True,

    hide_index=True

)



st.divider()



# =====================================
# PER GURU
# =====================================


st.subheader(
    "👨‍🏫 Jadwal Per Guru"
)


guru = st.selectbox(

    "Pilih Guru",

    jadwal["Guru"].unique()

)



st.dataframe(

    jadwal[
        jadwal["Guru"] == guru
    ],

    use_container_width=True,

    hide_index=True

)
