import streamlit as st
import requests
import time

# --- CONFIGURATION ---
RAW_TOKEN = "pat5Agw2Boueul8Xr.58d6e1c0de6e50dd5edefc64b0d1500389804a8ecaa48fda5b7249e7b2dd3ab8"
AIRTABLE_TOKEN = RAW_TOKEN.strip()
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1" 

st.set_page_config(page_title="AI Sync Pro", page_icon="🚀", layout="wide")

# CSS: Text box ko bada aur readable banane ke liye
st.markdown("""
<style>
    .stCode { 
        border: 2px solid #4A90E2 !important; 
        border-radius: 10px !important;
    }
    /* Code block ki height badhane ke liye custom CSS */
    .stCode > div {
        min-height: 300px !important;
    }
    .main {
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Sync: Mobile to PC")

URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}

def fetch_data():
    # Naya data sabse upar dikhane ke liye
    params = {"sort[0][field]": "Time", "sort[0][direction]": "desc"}
    try:
        res = requests.get(URL, headers=HEADERS, params=params)
        return res.json().get('records', []) if res.status_code == 200 else []
    except:
        return []

records = fetch_data()

if not records:
    st.info("Waiting for data from mobile... Share something from your phone!")
else:
    for record in records:
        fields = record.get('fields', {})
        content = fields.get('Content', "No text")
        timestamp = fields.get('Time', "Unknown")

        with st.container():
            st.caption(f"📅 Received: {timestamp}")
            
            # st.code use karne se top-right mein COPY ICON apne aap aayega
            # language='python' rakha hai taaki code high-light ho, normal text ke liye bhi ye bada dikhega
            st.code(content, language='python', wrap_lines=True)
            
            # Agar koi file (jaise .py file) attach ho
            if 'FileAttachments' in fields:
                for file in fields['FileAttachments']:
                    st.download_button(
                        label=f"📥 Download {file['filename']}",
                        data=requests.get(file['url']).content,
                        file_name=file['filename']
                    )
            st.markdown("---")

# Auto-refresh har 5 second mein
time.sleep(5)
st.rerun()
