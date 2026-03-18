import streamlit as st
import requests
import time

# --- CONFIGURATION ---
RAW_TOKEN = "pat5Agw2Boueul8Xr.58d6e1c0de6e50dd5edefc64b0d1500389804a8ecaa48fda5b7249e7b2dd3ab8"
AIRTABLE_TOKEN = RAW_TOKEN.strip()
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1" 

st.set_page_config(page_title="AI Sync Pro", page_icon="🚀", layout="wide")

# CSS: Styling for better visibility and large code blocks
st.markdown("""
<style>
    .stCode { border: 2px solid #4A90E2 !important; border-radius: 10px !important; }
    .stCode > div { min-height: 250px !important; }
    .main { background-color: #f9f9f9; }
</style>
""", unsafe_allow_html=True)

URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}", "Content-Type": "application/json"}

# --- SECTION 1: SEND TO MOBILE ---
st.title("📤 Send to Mobile")
with st.expander("Write code or text to send to Phone", expanded=False):
    with st.form("send_form", clear_on_submit=True):
        to_send = st.text_area("Type/Paste here:", height=150)
        submitted = st.form_submit_button("Send to Mobile 📲")
        if submitted and to_send:
            res = requests.post(URL, headers=HEADERS, json={"records": [{"fields": {"Content": to_send}}]})
            if res.status_code == 200:
                st.success("Sent! Check Airtable app on your phone.")
            else:
                st.error("Failed to send.")

st.divider()

# --- SECTION 2: RECEIVE FROM MOBILE ---
st.title("📥 Received from Mobile (Auto-Sync)")

def fetch_data():
    # Latest 50 records fetching with Sort by Time
    params = {"sort[0][field]": "Time", "sort[0][direction]": "desc", "maxRecords": 50}
    try:
        res = requests.get(URL, headers={"Authorization": f"Bearer {AIRTABLE_TOKEN}"}, params=params)
        return res.json().get('records', []) if res.status_code == 200 else []
    except:
        return []

records = fetch_data()

if not records:
    st.info("Waiting for data... Share something from your iPhone Shortcut!")
else:
    for record in records:
        fields = record.get('fields', {})
        content = fields.get('Content', "No text")
        timestamp = fields.get('Time', "Unknown Time")

        with st.container(border=True):
            st.caption(f"🕒 Received: {timestamp}")
            # st.code provides an automatic COPY button in the top-right corner
            st.code(content, language='python', wrap_lines=True)
            
            # File Download Handling
            if 'FileAttachments' in fields:
                for file in fields['FileAttachments']:
                    st.download_button(label=f"📥 Download {file['filename']}", 
                                     data=requests.get(file['url']).content, 
                                     file_name=file['filename'])

# Auto-refresh every 7 seconds
time.sleep(7)
st.rerun()
