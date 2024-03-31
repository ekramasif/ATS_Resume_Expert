from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert", page_icon=":briefcase:", layout="wide")
st.title("ATS Tracking System")

# Sidebar
st.sidebar.title("ATS Resume Expert")
input_text = st.sidebar.text_area("Job Description: ", key="input")
uploaded_file = st.sidebar.file_uploader("Upload your resume(PDF)...", type=["pdf"])

submit1 = st.sidebar.button("Tell Me About the Resume")
submit3 = st.sidebar.button("Percentage Match")

# Main content area
col2 = st.columns([3])[0]

with col2:
    st.image("ats.jpg", use_column_width=True)  # Placeholder image

if submit1 or submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if submit1:
            input_prompt = """
            You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
            Please share your professional evaluation on whether the candidate's profile aligns with the role. 
            Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.

            after that you need to give information on this points
            1. Searchability
            2. Skills (Soft Skill and Hard Skill)
            3. Recruiter tips
            4. Formatting
            """
        else:
            input_prompt = """
            You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
            your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
            the job description. First, the output should come as a percentage and then keywords missing and last final thoughts.
            """

        response = get_gemini_response(input_text, pdf_content, input_prompt)
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please upload the resume to proceed.")
