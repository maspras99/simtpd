import streamlit as st
from datetime import datetime
import sqlite3

conn = sqlite3.connect('tpd_data.db', check_same_thread=False)
c = conn.cursor()

st.title("Majelis TPD - SIM Tim Pemilihan Daerah")
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Proses Notifikasi dari Pimpinan DKPP")

c.execute("SELECT nama_majelis, timestamp FROM majelis_data WHERE status = 'Approved by Pimpinan' ORDER BY id DESC LIMIT 1")
latest_data = c.fetchone()
nama_majelis = st.text_input("Nama Majelis dari Pimpinan DKPP", value=latest_data[0] if latest_data else "")
action = st.selectbox("Pilih Aksi", ["Proses Notifikasi", "Menolak", "Terima"])
if st.button("Proses Majelis TPD"):
    if nama_majelis:
        if action == "Terima":
            c.execute("UPDATE majelis_data SET status = 'Accepted by Majelis', timestamp = ? WHERE nama_majelis = ?", 
                      (datetime.now().strftime('%H:%M %d/%m/%Y'), nama_majelis))
            conn.commit()
            st.session_state.result = f"Majelis TPD menerima notifikasi penunjukkan untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
            st.session_state.staff_result = f"Notifikasi diterima dari Majelis TPD untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
        elif action == "Menolak":
            c.execute("UPDATE majelis_data SET status = 'Rejected by Majelis', timestamp = ? WHERE nama_majelis = ?", 
                      (datetime.now().strftime('%H:%M %d/%m/%Y'), nama_majelis))
            conn.commit()
            st.session_state.result = f"Majelis TPD menolak notifikasi penunjukkan untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
            rejection_letter = f"""
            <div class="rejection-letter">
                <h3>Surat Penolakan</h3>
                <p>Kepada Yth. Admin TPD</p>
                <p>Tanggal: {datetime.now().strftime('%A, %d %B %Y %H:%M')} WIB</p>
                <p>Dengan hormat,</p>
                <p>Sehubungan dengan notifikasi penunjukkan, Majelis TPD menyatakan penolakan terhadap usulan {nama_majelis}. Mohon menindaklanjuti.</p>
                <p>Hormat kami,</p>
                <p>Majelis TPD</p>
            </div>
            """
            st.markdown(rejection_letter, unsafe_allow_html=True)
        else:
            st.session_state.result = f"Majelis TPD memproses notifikasi penunjukkan untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
    else:
        st.session_state.result = "Tidak ada data Majelis untuk diproses."

if st.session_state.get("result", "").startswith("Majelis TPD menerima"):
    if st.button("Resume Hasil Sidang"):
        st.session_state.result = f"Resume Hasil Sidang dibuat untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
    if st.button("Chat ke Staf DKPP"):
        st.session_state.result = f"Chat ke Staf DKPP dimulai untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."

st.markdown(f'<div class="result">{st.session_state.result}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)