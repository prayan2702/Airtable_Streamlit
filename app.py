import streamlit as st
import requests
import os
from datetime import datetime
import pytz

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
        utc_dt = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.000Z")
        utc_dt = pytz.utc.localize(utc_dt)
        ist_tz = pytz.timezone('Asia/Kolkata')
        ist_dt = utc_dt.astimezone(ist_tz)
        return ist_dt.strftime("%d %b %Y, %I:%M %p")
    except:
        return utc_time_str

# Cached fetch - sirf tab call hoga jab manually refresh karo
# ttl=300 matlab 5 minute tak same data use karega (extra safety)
@st.cache_data(ttl=300)
def fetch_data():
    params = {"sort[0][field]": "Time", "sort[0][direction]": "desc", "maxRecords": 20}
    res = requests.get(URL, headers={"Authorization": f"Bearer {AIRTABLE_TOKEN}"}, params=params)
    return res.json().get('records', []) if res.status_code == 200 else []

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
                if res.status_code == 200:
                    st.success("Sent! ✅")
                    # Send ke baad cache clear karo taaki naya data dikhe
                    fetch_data.clear()

    st.divider()

    # Header row: subheading + refresh button ek line mein
    col_title, col_btn = st.columns([5, 1])
    with col_title:
        st.subheader("📥 Received from AI / Mobile")
    with col_btn:
        st.write("")  # spacing
        if st.button("🔄 Refresh", use_container_width=True):
            fetch_data.clear()  # Cache clear karo, fresh API call hogi
            st.rerun()

    records = fetch_data()

    if not records:
        st.info("Koi records nahi mili. Refresh karo.")
    else:
        for record in records:
            fields = record.get('fields', {})
            content = fields.get('Content', "")
            raw_time = fields.get('Time', "")
            local_time = format_time(raw_time)

            with st.container(border=True):
                st.caption(f"🕒 {local_time} (IST)")
                st.code(content, language='python', wrap_lines=False)

with tab2:
    uploaded_files = st.file_uploader("Upload files:", accept_multiple_files=True)
    if uploaded_files:
        for f in uploaded_files:
            with open(os.path.join(UPLOAD_FOLDER, f.name), "wb") as file:
                file.write(f.getbuffer())
        st.success(f"Uploaded {len(uploaded_files)} files! ✅")

    for file in os.listdir(UPLOAD_FOLDER):
        col1, col2 = st.columns([4, 1])
        with col1:
            with open(os.path.join(UPLOAD_FOLDER, file), "rb") as f:
                st.download_button(label=f"⬇️ {file}", data=f.read(), file_name=file, key=f"dl_{file}")
        with col2:
            if st.button("🗑️", key=f"del_{file}"):
                os.remove(os.path.join(UPLOAD_FOLDER, file))
                st.rerun()

# ❌ REMOVED: time.sleep(15) aur st.rerun() - ye API limit khatam kar raha tha
