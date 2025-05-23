from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load API key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Function to generate response from Gemini AI model
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Function to convert uploaded PDF resume to image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert", page_icon=":briefcase:", layout="wide", menu_items=None)

# Custom CSS for enhanced design
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

  /* Sidebar styles */
  .sidebar-container {
    background-color: #f8f8f8;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  .sidebar-title {
    font-family: 'Arial', sans-serif;
    color: #333333;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
  }
  .sidebar-text {
    font-family: 'Arial', sans-serif;
    color: #666666;
    font-size: 16px;
  }

  /* Footer styles */
  .footer {
    background-color: #333333;
    color: #ffffff;
    padding: 10px 0;
    width: 100%;
    text-align: center;
    font-family: 'Arial', sans-serif;
    font-size: 14px;
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 1;
  }

  /* Main content styles */
  .main-content {
    margin-left: 300px; /* Sidebar width */
    padding-bottom: 60px; /* Footer height */
  }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar.container():
    st.markdown('<div class="sidebar-title">ATS Resume Expert</div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text">Submit your resume and job description for analysis.</p>', unsafe_allow_html=True)
    input_text = st.text_area("Job Description: ", key="input")
    uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

    # Create a form to contain the inputs and submit button
    with st.form(key='my_form'):
        submit1 = st.form_submit_button("Tell Me About the Resume")
        submit3 = st.form_submit_button("Percentage Match")
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area
with st.container():
    col2 = st.columns([3])[0]
    # Placeholder image
    with col2:
        st.image("ATS.jpg", use_container_width=True)

# Handle button clicks
if submit1 or submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if submit1:
            # Prompt for resume analysis
            input_prompt = """
            You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
            Please share your professional evaluation on whether the candidate's profile aligns with the role.
            Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.

            After that, please provide information on the following points:
            1. Searchability
            2. Skills (Soft Skill and Hard Skill)
            3. Recruiter tips
            4. Formatting
            """
        else:
            # Prompt for percentage match
            input_prompt = """
            You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
            Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume matches
            the job description. First, the output should come as a percentage, then keywords missing, and lastly, final thoughts.
            """

        # Show loading spinner while generating response
        with st.spinner('Generating response...'):
            # Generate response from Gemini AI model
            response = get_gemini_response(input_text, pdf_content, input_prompt)

        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please upload the resume to proceed.")

# Footer
st.markdown("""
<div class="footer" id="footer">
  <p>&copy; 2024 ATS Resume Expert. All rights reserved. | Developed by <a href="https://www.linkedin.com/in/ekram-asif/">Md Ekram Uddin</a></p>
</div>
""", unsafe_allow_html=True)
