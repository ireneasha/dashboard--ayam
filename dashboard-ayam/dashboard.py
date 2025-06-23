import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Dashboard Peternakan Ayam", layout="wide")

st.title("🐔 Dashboard Harian Peternakan Ayam")

columns = [
    "Tanggal",
    "Ayam Masuk",
    "Ayam Mati",
    "Populasi Aktif",
    "Telur Diproduksi",
    "Telur Rusak",
    "Persentase Rusak (%)",
    "Konsumsi Pakan (kg)",
    "Vaksinasi",
]

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=columns)

st.subheader("Input Harian")
tanggal = st.date_input("Tanggal", date.today())
ayam_masuk = st.number_input("Ayam Masuk (ekor)", min_value=0, value=0)
ayam_mati = st.number_input("Ayam Mati (ekor)", min_value=0, value=0)

# Hitung Populasi Aktif dari entri terakhir
pop_aktif_prev = (
    st.session_state.data["Populasi Aktif"].iloc[-1]
    if not st.session_state.data.empty
    else 0
)

pop_aktif = max(pop_aktif_prev + ayam_masuk - ayam_mati, 0)

telur_produksi = st.number_input("Telur Diproduksi (butir)", min_value=0, value=0)
telur_rusak = st.number_input("Telur Rusak (butir)", min_value=0, value=0)
pakan = st.number_input("Konsumsi Pakan (kg)", min_value=0.0, value=0.0, step=0.1)
vaksin = st.text_input("Vaksinasi (nama/dosis)")

if st.button("Simpan Data"):
    persentase_rusak = (telur_rusak / telur_produksi) * 100 if telur_produksi > 0 else 0
    new_row = {
        "Tanggal": tanggal,
        "Ayam Masuk": ayam_masuk,
        "Ayam Mati": ayam_mati,
        "Populasi Aktif": pop_aktif,
        "Telur Diproduksi": telur_produksi,
        "Telur Rusak": telur_rusak,
        "Persentase Rusak (%)": round(persentase_rusak, 2),
        "Konsumsi Pakan (kg)": pakan,
        "Vaksinasi": vaksin,
    }
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)

st.subheader("Data Harian")
st.dataframe(st.session_state.data)

if not st.session_state.data.empty:
    total_ayam = st.session_state.data["Populasi Aktif"].iloc[-1]
    total_telur = st.session_state.data["Telur Diproduksi"].sum()
    total_rusak = st.session_state.data["Telur Rusak"].sum()
    avg_rusak = st.session_state.data["Persentase Rusak (%)"].mean()
    total_pakan = st.session_state.data["Konsumsi Pakan (kg)"].sum()

    st.subheader("📊 Ringkasan")
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Populasi Aktif", total_ayam)
    col2.metric("Total Telur", total_telur)
    col3.metric("Total Rusak", total_rusak)
    col4.metric("Rata-rata Persentase Rusak (%)", f"{avg_rusak:.2f}%")
    col5.metric("Total Konsumsi Pakan (kg)", total_pakan)
    