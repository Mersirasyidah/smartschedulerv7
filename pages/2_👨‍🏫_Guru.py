import streamlit as st
from database import load_database

st.set_page_config(
    page_title="Data Guru",
    page_icon="👨‍🏫",
    layout="wide"
)

db = load_database()

st.title("👨‍🏫 Data Guru")

if "Guru" in db:

    guru = db["Guru"]

    st.metric("Jumlah Guru", len(guru))

    keyword = st.text_input(
        "Cari Nama Guru"
    )

    if keyword:

        guru = guru[
            guru["Nama Guru"].str.contains(
                keyword,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        guru,
        use_container_width=True,
        hide_index=True
    )

else:

    st.error("Sheet Guru tidak ditemukan")
