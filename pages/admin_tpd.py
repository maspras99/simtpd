import streamlit as st
from datetime import datetime, timedelta
import sqlite3

# Connect to SQLite database (already initialized in main app)
conn = sqlite3.connect('tpd_data.db', check_same_thread=False)
c = conn.cursor()

st.title("Admin TPD - SIM Tim Pemilihan Daerah")
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Input Data Majelis TPD")

nama_majelis = st.text_input("Masukkan Nama Majelis")
if st.button("GET DATA PENJADWALAN SIDANG (API Dashboard)"):
    st.session_state.result = f"Data penjadwalan sidang diambil dari API Dashboard pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
if st.button("Input Nama Majelis Pada Jadwal Sidang"):
    st.session_state.result = f"Verifikasi nama majelis: {nama_majelis} selesai pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
if st.button("Kirim Nama Majelis TPD ke Kabag/Kasubag"):
    if nama_majelis:
        c.execute("INSERT INTO majelis_data (nama_majelis, status, timestamp) VALUES (?, ?, ?)", 
                  (nama_majelis, "Sent to Kabag", datetime.now().strftime('%H:%M %d/%m/%Y')))
        conn.commit()
        st.session_state.result = f"Nama Majelis TPD: {nama_majelis} dikirim ke Kabag/Kasubag pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB. Menunggu verifikasi dari Kabag."
    else:
        st.session_state.result = "Masukkan nama Majelis terlebih dahulu."
if st.button("Notifikasi ke Majelis TPD"):
    st.session_state.result = f"Notifikasi dikirim ke Majelis TPD pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
if st.button("Upload Surat Penunjukkan Majelis TPD"):
    st.session_state.result = f"Surat Penunjukkan Majelis TPD diunggah pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
if st.button("Jika Sidang Selesai Kirim Notifikasi Majelis TPD Harus Upload Resume Max 2 Hari Kerja"):
    deadline = datetime.now() + timedelta(days=2)
    deadline_str = deadline.strftime("%A, %d %B %Y")
    st.session_state.result = f"Notifikasi dikirim: Majelis TPD wajib mengunggah resume maksimal 2 hari kerja, yaitu {deadline_str} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."

st.markdown(f'<div class="result">{st.session_state.result}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)