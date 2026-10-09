import os
import streamlit as st
import pypdf
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="ATS Resume Checker",
    page_icon="📄",
    layout="wide"
)

# Configure Gemini API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)

st.title("📄 ATS Resume Evaluation & Improvement Tool")
st.write("Upload your resume and optional job description to get an ATS Score and feedback.")

# Input layout
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])

with col2:
    job_description = st.text_area("Job Description (Optional, recommended for accurate matching)", height=150)

def extract_pdf_text(file):
    reader = pypdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

if st.button("Evaluate Resume"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not uploaded_file:
        st.warning("Please upload a resume in PDF format.")
    else:
        with st.spinner("Analyzing resume with Gemini..."):
            try:
                # Extract text
                resume_text = extract_pdf_text(uploaded_file)
                
                # Initialize Gemini Model
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Build Prompt
                prompt = f"""
                You are an expert Applicant Tracking System (ATS) scanner and recruitment manager.
                Evaluate the following resume text against the provided job description (if available).
                
                Resume Content:
                {resume_text}
                
                Job Description Context:
                {job_description if job_description else "No specific job description provided. Evaluate based on general professional ATS standards."}
                
                Provide a structured report with:
                1. **ATS Score**: (Rating out of 100%)
                2. **Overall Summary**: Concise assessment of strengths.
                3. **Missing Keywords / Skills**: Core hard/soft skills missing or requiring emphasis.
                4. **Formatting & Structure Issues**: Any ATS parsing concerns.
                5. **Actionable Improvement Suggestions**: Bullet points for immediate improvements.
                """
                
                response = model.generate_content(prompt)
                
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")