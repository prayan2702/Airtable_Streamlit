import streamlit as st
import requests
import time
import os
import shutil
from datetime import datetime
import pytz  # Timezone convert karne ke liye

# --- CONFIGURATION ---
RAW_TOKEN = "pat5Agw2Boueul8Xr.58d6e1c0de6e50dd5edefc64b0d1500389804a8ecaa48fda5b7249e7b2dd3ab8"
AIRTABLE_TOKEN = RAW_TOKEN.strip()
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1" 
URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}", "Content-Type": "application/json"}
UPLOAD_FOLDER = "shared_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="AI Bridge Pro", page_icon="🚀", layout="wide")

# Time format function (UTC to IST)
def format_time(utc_time_str):
    try:
        # Airtable UTC format: '2026-03-18T17:53:53.000Z'
        utc_dt = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.000Z")
        utc_dt = pytz.utc.localize(utc_dt)
        ist_tz = pytz.timezone('Asia/Kolkata')
        ist_dt = utc_dt.astimezone(ist_tz)
        return ist_dt.strftime("%d %b %Y, %I:%M %p") # Example: 18 Mar 2026, 11:23 PM
    except:
        return utc_time_str

st.title("🚀 AI Bridge: Universal Sync")
tab1, tab2 = st.tabs(["📋 AI Sync (Airtable)", "📂 File Sharing"])

with tab1:
    st.subheader("📤 Send to Mobile")
    with st.expander("Write code or text to send"):
        with st.form("send_form", clear_on_submit=True):
            to_send = st.text_area("Type/Paste here:", height=150)
            submitted = st.form_submit_button("Send to Mobile 📲")
            if submitted and to_send:
                res = requests.post(URL, headers=HEADERS, json={"records": [{"fields": {"Content": to_send}}]})
                if res.status_code == 200: st.success("Sent!")

    st.divider()
    st.subheader("📥 Received from AI / Mobile")

    def fetch_data():
        params = {"sort[0][field]": "Time", "sort[0][direction]": "desc", "maxRecords": 20}
        res = requests.get(URL, headers={"Authorization": f"Bearer {AIRTABLE_TOKEN}"}, params=params)
        return res.json().get('records', []) if res.status_code == 200 else []

    records = fetch_data()
    for record in records:
        fields = record.get('fields', {})
        content = fields.get('Content', "")
        raw_time = fields.get('Time', "")
        
        # YAHAN LOCAL TIME DIKHEGA
        local_time = format_time(raw_time) 
        
        with st.container(border=True):
            st.caption(f"🕒 {local_time} (IST)")
            st.code(content, language='python', wrap_lines=False)

with tab2:
    # Multiple file upload support
    uploaded_files = st.file_uploader("Upload files:", accept_multiple_files=True)
    if uploaded_files:
        for f in uploaded_files:
            with open(os.path.join(UPLOAD_FOLDER, f.name), "wb") as file:
                file.write(f.getbuffer())
        st.success(f"Uploaded {len(uploaded_files)} files!")
    
    # File display and delete logic remains same
    for file in os.listdir(UPLOAD_FOLDER):
        col1, col2 = st.columns([4, 1])
        with col1:
            with open(os.path.join(UPLOAD_FOLDER, file), "rb") as f:
                st.download_button(label=f"⬇️ {file}", data=f.read(), file_name=file, key=f"dl_{file}")
        with col2:
            if st.button(f"🗑️", key=f"del_{file}"):
                os.remove(os.path.join(UPLOAD_FOLDER, file))
                st.rerun()

time.sleep(15)
st.rerun()
