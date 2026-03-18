import streamlit as st
import requests
import time

# --- CONFIGURATION ---
RAW_TOKEN = "pat5Agw2Boueul8Xr.58d6e1c0de6e50dd5edefc64b0d1500389804a8ecaa48fda5b7249e7b2dd3ab8"
AIRTABLE_TOKEN = RAW_TOKEN.strip()
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1" 

st.set_page_config(page_title="AI Bridge", page_icon="📲")
st.title("📲 Mobile to PC: AI Sync")

# API URL aur Headers
URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}

# Data fetch karne ka function
def fetch_airtable_data():
    try:
        # Sort by Created Time (descending) taaki naya message sabse upar dikhe
        params = {"sort[0][field]": "Time", "sort[0][direction]": "desc"}
        response = requests.get(URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json().get('records', [])
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return []
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []

# Placeholder taaki refresh hone par screen jhatka na mare
placeholder = st.empty()

with placeholder.container():
    records = fetch_airtable_data()
    if not records:
        st.info("Airtable mein koi data nahi mila. Mobile se bhej kar dekhein!")
    else:
        # Sabse naya record dikhana
        for record in records:
            fields = record.get('fields', {})
            content = fields.get('Content', fields.get('Contenrt', "No text available"))
            timestamp = fields.get('Time', "Unknown time")
            
            st.markdown(f"**🕒 Time:** {timestamp}")
            st.info(content)
            
            if 'FileAttachments' in fields:
                for file in fields['FileAttachments']:
                    st.image(file['url'], use_container_width=True)
            st.divider()

# --- AUTO REFRESH LOGIC ---
# Har 5 second mein apne aap refresh hoga
time.sleep(5)
st.rerun()
