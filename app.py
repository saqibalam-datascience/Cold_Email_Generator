import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import get_website_jd, get_llm, resume_extractor, get_template
from portfolio import Portfolio
from utils import clean_text, pdf_extractor


def create_streamlit_app():
    st.set_page_config(layout="wide", page_title="Cold Email / Cover letter Generator", page_icon="📧")
    st.title("📧 Cold Email / Cover letter Generator")

    # Streamlit Sidebar - User enters Google API Key
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

    # Upload Resume
    resume_file = st.file_uploader("Upload your Resume (PDF only)", type=['pdf'])
    
    # Mode Selection
    input_mode = st.selectbox("Select Input Mode", ['Job Description', 'Job URL'])

    job_input = ""
    if input_mode == 'Job Description':
        job_input = st.text_area("Paste the Job Description:", height=300)
    elif input_mode == 'Job URL':
        job_input = st.text_input("Enter the Job URL:")

    submit_button = st.button("Generate Template")

    if submit_button:
        try:
            if job_input is None:
                st.error("Please Enter a Job Description or URL.")
                st.stop()
            llm = get_llm(api_key)

            if resume_file is not None:
                # Extract text from the uploaded PDF resume
                resume_content = pdf_extractor(resume_file)
                clean_text_resume = clean_text(resume_content)
                resume_KTs = resume_extractor(clean_text_resume, llm)
            else:
                st.error("Please upload a PDF resume.")
            
            

            if input_mode == 'Job URL':
                loader = WebBaseLoader([job_input])
                jd = clean_text(loader.load()[0].page_content)
                if not jd:
                    st.error("Please enter a valid job URL or paste the Job Description directly.")
                cleaned_jd = get_website_jd(jd, llm)
                cleaned_jd = clean_text(cleaned_jd)

            elif input_mode == 'Job Description':
                cleaned_jd = clean_text(job_input)
                if not cleaned_jd:
                    st.error("Please enter a Job Description.")
            
            cover_letter = get_template(cleaned_jd, resume_KTs, llm)
            st.text(cover_letter)


        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    create_streamlit_app()