import streamlit as st
import requests

# --- CONFIGURATION ---
# Token ke aage peeche koi space na rahe isliye .strip() use kiya hai
RAW_TOKEN = "pat5Agw2Boueul8Xr.58d6e1c0de6e50dd5edefc64b0d1500389804a8ecaa48fda5b7249e7b2dd3ab8"
AIRTABLE_TOKEN = RAW_TOKEN.strip()
BASE_ID = "app3tvRmLUYUWw3cM"
TABLE_NAME = "Table 1" 

st.set_page_config(page_title="AI Bridge", page_icon="📲")
st.title("📲 Mobile to PC: AI Sync")

# API URL aur Headers (f-string ka dhyan rakhein)
URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}

try:
    # Testing purpose ke liye headers ko check karte hain
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json().get('records', [])
        if not data:
            st.info("Airtable mein koi data nahi mila. Ek row add karein!")
        else:
            for record in data:
                fields = record.get('fields', {})
                # Column names check karein: Content ya Contenrt?
                content = fields.get('Content', fields.get('Contenrt', "No text available"))
                
                st.subheader("📝 Latest Content:")
                st.info(content)
                
                if 'FileAttachments' in fields:
                    st.write("📎 Attached Files:")
                    for file in fields['FileAttachments']:
                        st.image(file['url'])
    
    elif response.status_code == 401:
        st.error("Error 401: Authentication Failed. Token sahi se copy nahi hua ya format galat hai.")
        st.write("Tip: Ek baar Airtable mein naya token bana kar dekhein.")
    elif response.status_code == 404:
        st.error(f"Error 404: Table '{TABLE_NAME}' nahi mila. Name check karein.")
    else:
        st.error(f"Error {response.status_code}: {response.text}")

except Exception as e:
    st.error(f"Something went wrong: {e}")
