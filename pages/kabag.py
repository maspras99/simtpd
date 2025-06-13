import streamlit as st
from datetime import datetime
import sqlite3

conn = sqlite3.connect('tpd_data.db', check_same_thread=False)
c = conn.cursor()

st.title("Kabag - SIM Tim Pemilihan Daerah")
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Verifikasi Data dari Admin TPD")

c.execute("SELECT nama_majelis, timestamp FROM majelis_data WHERE status = 'Sent to Kabag' ORDER BY id DESC LIMIT 1")
latest_data = c.fetchone()
nama_majelis = st.text_input("Nama Majelis dari Admin TPD", value=latest_data[0] if latest_data else "")
if st.button("Verifikasi Kabag"):
    if nama_majelis:
        c.execute("UPDATE majelis_data SET status = 'Verified by Kabag', timestamp = ? WHERE nama_majelis = ?", 
                  (datetime.now().strftime('%H:%M %d/%m/%Y'), nama_majelis))
        conn.commit()
        st.session_state.result = f"Verifikasi oleh Kabag selesai untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB. Data dikirim ke Kasubag."
        st.session_state.kasubag_result = f"Data dari Kabag diterima untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
    else:
        st.session_state.result = "Tidak ada data Majelis untuk diverifikasi."

st.markdown(f'<div class="result">{st.session_state.result}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)