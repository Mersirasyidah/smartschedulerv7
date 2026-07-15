import streamlit as st
from database import load_database

st.title("🏫 Data Rombel")

db = load_database()

if "Rombel" in db:

    rombel = db["Rombel"]

    st.metric("Jumlah Rombel", len(rombel))

    st.dataframe(
        rombel,
        use_container_width=True,
        hide_index=True
    )

else:

    st.error("Sheet Rombel tidak ditemukan")
