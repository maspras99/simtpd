import streamlit as st
from datetime import datetime
import sqlite3

conn = sqlite3.connect('tpd_data.db', check_same_thread=False)
c = conn.cursor()

st.title("Draft TA - SIM Tim Pemilihan Daerah")
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Proses Dokumen dari Staff TPD")

c.execute("SELECT nama_majelis, timestamp FROM majelis_data WHERE status = 'Document Created' ORDER BY id DESC LIMIT 1")
latest_data = c.fetchone()
nama_majelis = st.text_input("Nama Majelis dari Staff TPD", value=latest_data[0] if latest_data else "")
if st.button("Resume Sidang"):
    if nama_majelis:
        c.execute("UPDATE majelis_data SET status = 'Archived by Draft TA', timestamp = ? WHERE nama_majelis = ?", 
                  (datetime.now().strftime('%H:%M %d/%m/%Y'), nama_majelis))
        conn.commit()
        st.session_state.result = f"Resume Di Cek Dan Arsip oleh Draft TA untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."

st.markdown(f'<div class="result">{st.session_state.result}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)