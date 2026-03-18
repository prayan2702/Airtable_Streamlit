import streamlit as st
import requests
import time

# --- APNI DETAILS YAHAN BHAREIN ---
AIRTABLE_TOKEN = "patY5mgE1F7z0NPca.a84cffc9f635dad84c6de8b2bc6067231df166124a191b057c9ff32195b79fa6"
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1" # Agar naam badla hai toh wo likhein

URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}

st.set_page_config(page_title="AI Bridge", page_icon="📲")
st.title("📲 Mobile to PC: AI Sync & File Transfer")

# Refresh mechanism ke liye empty space
placeholder = st.empty()

while True:
    # Latest record fetch karna (Time ke hisaab se)
    params = {"sort[0][field]": "Created Time", "sort[0][direction]": "desc", "maxRecords": 1}
    
    try:
        response = requests.get(URL, headers=HEADERS, params=params)
        
        with placeholder.container():
            if response.status_code == 200:
                records = response.json().get('records', [])
                if records:
                    fields = records[0]['fields']
                    
                    # 1. Chat/Text Section
                    st.subheader("📝 Latest AI Chat:")
                    content = fields.get('Content', 'No text available')
                    st.info(content)
                    st.button("Copy to Clipboard", on_click=lambda: st.write("Text copied (Manually select and copy)"))

                    # 2. File Section
                    attachments = fields.get('FileAttachment')
                    if attachments:
                        st.subheader("📎 Attached Files:")
                        for file in attachments:
                            file_url = file['url']
                            file_name = file['filename']
                            file_data = requests.get(file_url).content
                            st.download_button(label=f"📥 Download {file_name}", 
                                             data=file_data, 
                                             file_name=file_name)
                    else:
                        st.write("No files attached.")
                        
                    st.caption(f"Last updated: {fields.get('Created Time')}")
                else:
                    st.warning("Awaiting data from iPhone...")
            else:
                st.error(f"Error: {response.status_code}. Check API Token/Base ID.")

    except Exception as e:
        st.error(f"Connection error: {e}")

    # 10 second wait karke automatically refresh karega
    time.sleep(10)
    st.rerun()
