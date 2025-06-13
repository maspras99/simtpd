import streamlit as st
from datetime import datetime, timedelta
import sqlite3

# CSS for styling
st.set_page_config(page_title="SIM Tim Pemilihan Daerah", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background-color: #f0f2f5; }
    .section { background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
    .button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
    .button:hover { background-color: #45a049; }
    .result { color: #2c3e50; font-size: 16px; margin-top: 10px; }
    .rejection-letter { border: 1px solid #e74c3c; padding: 10px; background-color: #f5e8e8; border-radius: 5px; margin-top: 10px; }
    .table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    .table th { background-color: #3498db; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize or connect to SQLite database
conn = sqlite3.connect('tpd_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS majelis_data 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, nama_majelis TEXT, status TEXT, timestamp TEXT)''')
conn.commit()

# Sidebar for page navigation
st.sidebar.title("SIM TPD Navigation")
pages = {
    "Admin TPD": "pages/admin_tpd",
    "Kabag": "pages/kabag",
    "Kasubag": "pages/kasubag",
    "Pimpinan DKPP": "pages/pimpinan_dkpp",
    "Majelis TPD": "pages/majelis_tpd",
    "Staff TPD": "pages/staff_tpd",
    "Draft TA": "pages/draft_ta"
}
selection = st.sidebar.selectbox("Pilih Role", list(pages.keys()))
page = pages[selection]
st.session_state.page = page

# Common session state initialization
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'notification_count' not in st.session_state:
    st.session_state.notification_count = 0
if 'eval_visible' not in st.session_state:
    st.session_state.eval_visible = False

# Load the selected page
with open(page + ".py", "r", encoding="utf-8") as f:
    page_code = f.read()
exec(page_code)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#7f8c8d;'>Simulasi dijalankan pada {datetime.now().strftime('%H:%M %d/%m/%Y')} WIB</p>", unsafe_allow_html=True)

# Close connection on app shutdown
def on_shutdown():
    conn.close()
import atexit
atexit.register(on_shutdown)