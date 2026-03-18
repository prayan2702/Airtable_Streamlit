import streamlit as st
import requests

# --- CONFIGURATION ---
# Token ko "Bearer " ke sath likhna zaroori hai
AIRTABLE_TOKEN = "paty5mgE1F7z0NPca.a84cff9f635dad84c6de8b2bc6067231df166124a191b057c9ff32195b79fa6"
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1"  # Aapki photo mein yahi naam hai

st.set_page_config(page_title="AI Bridge", page_icon="📲")
st.title("📲 Mobile to PC: AI Sync")

# API URL aur Headers
URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}

try:
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json().get('records', [])
        if not data:
            st.info("Airtable mein koi data nahi mila. Ek row add karein!")
        else:
            for record in data:
                fields = record.get('fields', {})
                # Aapke columns ke naam: 'Content', 'FileAttachments'
                content = fields.get('Content', "No text")
                st.subheader("📝 Latest Content:")
                st.info(content)
                
                if 'FileAttachments' in fields:
                    st.write("📎 Attached Files:")
                    for file in fields['FileAttachments']:
                        st.image(file['url']) # Agar image hai toh dikhayega
    
    elif response.status_code == 403:
        st.error("Error 403: Permission Denied. Token Scopes check karein (read/write access).")
    elif response.status_code == 404:
        st.error("Error 404: Table Name galat hai. Code mein 'Table 1' hi rakhein.")
    else:
        st.error(f"Error {response.status_code}: {response.text}")

except Exception as e:
    st.error(f"Something went wrong: {e}")
