import streamlit as st
from datetime import datetime
import sqlite3

conn = sqlite3.connect('tpd_data.db', check_same_thread=False)
c = conn.cursor()

st.title("Staff TPD - SIM Tim Pemilihan Daerah")
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Tugas Staff TPD")

c.execute("SELECT nama_majelis, timestamp FROM majelis_data WHERE status = 'Accepted by Majelis' ORDER BY id DESC LIMIT 1")
latest_data = c.fetchone()
nama_majelis = st.text_input("Nama Majelis dari Majelis TPD", value=latest_data[0] if latest_data else "")
if st.button("Buat Surat Penunjukkan"):
    if nama_majelis:
        c.execute("UPDATE majelis_data SET status = 'Document Created', timestamp = ? WHERE nama_majelis = ?", 
                  (datetime.now().strftime('%H:%M %d/%m/%Y'), nama_majelis))
        conn.commit()
        st.session_state.result = f"Surat penunjukkan dibuat via SRIKANDI untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
        st.session_state.draft_result = f"Surat penunjukkan dari Staff TPD diterima untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
if st.button("Notifikasi (max 3 kali)"):
    if st.session_state.notification_count < 3:
        st.session_state.notification_count += 1
        st.session_state.result = f"Notifikasi ke TPD ke-{st.session_state.notification_count} dikirim untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."
        st.success(f"Notifikasi ke-{st.session_state.notification_count} berhasil.")
    else:
        st.session_state.result = f"Batas notifikasi (3 kali) tercapai pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."

if st.button("Nilai Kinerja Majelis TPD"):
    st.session_state.eval_visible = not st.session_state.eval_visible
    st.session_state.result = "Formulir penilaian kinerja Majelis TPD ditampilkan." if st.session_state.eval_visible else ""
if st.session_state.eval_visible:
    st.markdown('<table class="table">', unsafe_allow_html=True)
    st.markdown("<tr><th>ID</th><th>Indikator</th><th>Skor (1-10)</th></tr>", unsafe_allow_html=True)
    scores = {}
    for i in range(1, 13):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1: st.write(i)
        with col2: st.write(f"Indikator {i} (e.g., Kehadiran Rakor)")
        with col3: scores[f"score{i}"] = st.number_input(f"Skor {i}", min_value=1, max_value=10, key=f"score{i}")
    if st.button("Hitung Total Skor"):
        total = sum(scores.values())
        average = total / 12
        st.session_state.result = f"Total Skor: {total} | Rata-rata: {average:.2f}/10 untuk {nama_majelis} pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB."

st.markdown(f'<div class="result">{st.session_state.result}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)