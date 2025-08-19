import streamlit as st
import os
from pdf_processor import load_file

st.title("📄 Resume Reader & Scorer")

uploaded_file = st.file_uploader("Upload a resume (PDF)", type="pdf")

if uploaded_file is not None:
    # To work with your existing pdf_processor functions,
    # we can save the uploaded file to a temporary location.
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Success!")