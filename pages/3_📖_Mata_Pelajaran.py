import streamlit as st
from database import load_database

st.title("📖 Data Mata Pelajaran")

db = load_database()

if "Mapel" in db:

    mapel = db["Mapel"]

    st.metric("Jumlah Mata Pelajaran", len(mapel))

    st.dataframe(
        mapel,
        use_container_width=True,
        hide_index=True
    )

else:

    st.error("Sheet Mapel tidak ditemukan")
