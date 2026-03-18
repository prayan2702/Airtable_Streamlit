import streamlit as st
import requests
import time
import os
import shutil
from datetime import datetime

# --- CONFIGURATION (Airtable) ---
RAW_TOKEN = "pat5Agw2Boueul8Xr.58d6e1c0de6e50dd5edefc64b0d1500389804a8ecaa48fda5b7249e7b2dd3ab8"
AIRTABLE_TOKEN = RAW_TOKEN.strip()
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1" 
URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}", "Content-Type": "application/json"}

# --- CONFIGURATION (File Sharing) ---
UPLOAD_FOLDER = "shared_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="AI Bridge Pro", page_icon="🚀", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stCode { border: 2px solid #4A90E2 !important; border-radius: 10px !important; }
    .stCode > div { min-height: 200px !important; }
    .main { background-color: #f9f9f9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AI Bridge: Universal Sync")

tab1, tab2 = st.tabs(["📋 AI Sync (Airtable)", "📂 File Sharing"])

# --- TAB 1: AI SYNC ---
with tab1:
    st.subheader("📤 Send to Mobile")
    with st.expander("Write code or text to send", expanded=False):
        with st.form("send_form", clear_on_submit=True):
            to_send = st.text_area("Type/Paste here:", height=150)
            submitted = st.form_submit_button("Send to Mobile 📲")
            if submitted and to_send:
                res = requests.post(URL, headers=HEADERS, json={"records": [{"fields": {"Content": to_send}}]})
                if res.status_code == 200:
                    st.success("Sent to Airtable!")
                else:
                    st.error("Failed to send.")

    st.divider()
    st.subheader("📥 Received from AI / Mobile")

    def fetch_airtable_data():
        params = {"sort[0][field]": "Time", "sort[0][direction]": "desc", "maxRecords": 20}
        try:
            res = requests.get(URL, headers={"Authorization": f"Bearer {AIRTABLE_TOKEN}"}, params=params)
            return res.json().get('records', []) if res.status_code == 200 else []
        except: return []

    records = fetch_airtable_data()
    if records:
        for record in records:
            fields = record.get('fields', {})
            content = fields.get('Content', "")
            time_str = fields.get('Time', "Unknown")
            with st.container(border=True):
                st.caption(f"🕒 {time_str}")
                st.code(content, language='python', wrap_lines=False)

# --- TAB 2: LOCAL FILE SHARING (Multiple Files) ---
with tab2:
    st.subheader("📁 Transfer Files (Direct PC-Mobile)")
    
    # NEW: Multiple files enabled here
    uploaded_files = st.file_uploader("Choose files to upload (Multiple allowed):", type=None, accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            # Avoid re-writing the same file if it exists
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"✅ {len(uploaded_files)} files uploaded successfully!")

    st.divider()
    st.subheader("Available Files")
    files = os.listdir(UPLOAD_FOLDER)
    
    if not files:
        st.info("No files in shared folder.")
    else:
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            col1, col2 = st.columns([4, 1])
            
            with col1:
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download {file}",
                        data=f.read(),
                        file_name=file,
                        key=f"dl_{file}"
                    )
            with col2:
                if st.button(f"🗑️ Delete", key=f"del_{file}"):
                    os.remove(file_path)
                    st.rerun()

    if files:
        st.markdown("---")
        if st.button("🚨 Clear All Files", key="clear_all_files"):
            shutil.rmtree(UPLOAD_FOLDER)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            st.rerun()

# Auto-refresh optimized
time.sleep(15)
st.rerun()
