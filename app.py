import streamlit as st
import requests
import time

# --- CONFIGURATION ---
RAW_TOKEN = "pat5Agw2Boueul8Xr.58d6e1c0de6e50dd5edefc64b0d1500389804a8ecaa48fda5b7249e7b2dd3ab8"
AIRTABLE_TOKEN = RAW_TOKEN.strip()
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1" 

st.set_page_config(page_title="AI Bridge Pro", page_icon="🚀", layout="wide")
st.title("🚀 AI Sync: Mobile to PC")

URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}

def fetch_data():
    # Naya data sabse upar dikhane ke liye sort use kiya hai
    params = {"sort[0][field]": "Time", "sort[0][direction]": "desc"}
    res = requests.get(URL, headers=HEADERS, params=params)
    return res.json().get('records', []) if res.status_code == 200 else []

records = fetch_data()

if not records:
    st.info("Waiting for data from mobile...")
else:
    for record in records:
        fields = record.get('fields', {})
        content = fields.get('Content', "No text")
        timestamp = fields.get('Time', "")

        with st.container(border=True):
            st.write(f"📅 **Received:** {timestamp}")
            
            # Text area for easy selection
            st.text_area("Content:", content, height=150, key=record['id'])
            
            # Check if it's a Python code or long text
            if "import " in content or "def " in content:
                st.code(content, language='python')

            # File Attachment handle karna
            if 'FileAttachments' in fields:
                st.subheader("📎 Attached Files")
                for file in fields['FileAttachments']:
                    col1, col2 = st.columns([3, 1])
                    col1.write(f"📄 {file['filename']}")
                    # Download button for .py or any file
                    with open(file['url'], 'rb') as f:
                        col2.download_button("Download File", file['url'], file_name=file['filename'])

            st.divider()

# Auto-refresh every 5 seconds
time.sleep(5)
st.rerun()
