import streamlit as st
import requests
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables from the streamlit_app/.env file
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
load_dotenv(dotenv_path)

# Configure the page
st.set_page_config(page_title="Image to LaTeX", layout="centered")

# Get API URL from environment variables
API_URL = os.getenv("API_URL", "http://localhost:5050/api/generate")

# App title
st.title("📄 Image to LaTeX Converter")
st.write(
    "Easily convert images containing tables, equations, or formatted text into LaTeX code. "
    "This tool is ideal for researchers and academics."
)

# Layout
st.divider()
col1, col2 = st.columns([2, 1])

# File uploader
with col1:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image file (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

# Content type selector
with col2:
    st.header("Select Content Type")
    content_type = st.radio("Content type in the image:", ["table", "equation", "text"])

st.divider()

# Submit button
if st.button("🔄 Generate LaTeX Code"):
    if uploaded_file is not None and content_type:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        # Prepare the file for API request
        files = {"file": uploaded_file.getvalue()}
        data = {"type": content_type}

        with st.spinner("Processing your image..."):
            try:
                # Send request to the API
                response = requests.post(API_URL, files={"file": uploaded_file}, data=data)
                if response.status_code == 200:
                    result = response.json()
                    latex_code = result["latex"]

                    # Show success message and LaTeX code
                    st.success("🎉 LaTeX Code Generated Successfully!")
                    st.subheader("LaTeX Code")
                    st.code(latex_code, language="latex")
                else:
                    st.error(f"Error: {response.json().get('error', 'An unknown error occurred.')}")
            except Exception as e:
                st.error(f"Failed to connect to the API: {str(e)}")
    else:
        st.warning("⚠️ Please upload an image and select the content type.")

# Footer
st.divider()
st.caption("Developed with ❤️ for researchers and academics.")
