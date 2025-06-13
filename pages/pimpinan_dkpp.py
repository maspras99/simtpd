import streamlit as st
from datetime import datetime
import sqlite3

conn = sqlite3.connect('tpd_data.db', check_same_thread=False)
c = conn.cursor()

st.title("Pimpinan DKPP - SIM Tim Pemilihan Daerah")
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Verifikasi Data dari Kasubag")

c.execute("SELECT nama_majelis, timestamp FROM majelis_data WHERE status = 'Processed by Kasubag' ORDER BY id DESC LIMIT 1")
latest_data = c.fetchone()
nama_majelis = st.text_input("Nama Majelis dari Kasubag", value=latest_data[0] if latest_data else "")
action = st.selectbox("Pilih Aksi", ["Approved", "Reject"])
if st.button("Verifikasi Nama Majelis"):
    if nama_majelis:
        if action == "Approved":
            c.execute("UPDATE majelis_data SET status = 'Approved by Pimpinan', timestamp = ? WHERE nama_majelis = ?", 
                      (datetime.now().strftime('%H:%M %d/%m/%Y'), nama_majelis))
            conn.commit()
            st.session_state.result = f"Verifikasi nama majelis {nama_majelis} disetujui pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB. Proses dilanjutkan ke Majelis TPD."
            st.session_state.majelis_result = f"Data dari Pimpinan DKPP diterima untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
        else:
            c.execute("UPDATE majelis_data SET status = 'Rejected by Pimpinan', timestamp = ? WHERE nama_majelis = ?", 
                      (datetime.now().strftime('%H:%M %d/%m/%Y'), nama_majelis))
            conn.commit()
            st.session_state.result = f"Verifikasi nama majelis {nama_majelis} ditolak pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB. Dikembalikan ke Admin TPD."
            st.session_state.admin_result = f"Pengajuan nama majelis {nama_majelis} ditolak oleh Pimpinan DKPP. Mohon usulkan nama baru pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
    else:
        st.session_state.result = "Tidak ada data Majelis untuk diverifikasi."

st.markdown(f'<div class="result">{st.session_state.result}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)