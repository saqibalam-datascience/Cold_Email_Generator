import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_llm(groq_api):
    llm = ChatGroq(temperature=0, groq_api_key=groq_api, model_name="llama-3.3-70b-versatile")
    return llm

def resume_extractor(resume_text, llm):
    prompt_extract = PromptTemplate.from_template('''
    You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:

    1. Full Name
    2. Email Address
    3. Phone Number
    2. employment details (just company name and its duration)
    3. technical skills (either present in dedicated section or in projects worked on)
    4. Projects worked on summary (seperate column or section for each project's description with all quantitative details)
    5. education details
    6. certifications

    Resume:
    {resume}
    #Only return the valid text file format
    Example :
    Full Name
    Name of user
    NO PREAMBLE  
    ''')

    chain_extract = prompt_extract | llm
    resume_extract = chain_extract.invoke({"resume": resume_text})
    return resume_extract.content

def get_website_jd(website_content, llm):
    website_prompt_extract = PromptTemplate.from_template('''
    You are an AI bot designed to act as a professional for parsing job opening websites. You are given with website content and your job is to extract the following information from the content:

    1. Job Title
    2. Job Description
    3. Responsibilities
    4. Required Skills
    5. Qualification Required
    6. About the Company

    Website Content:
    {website_content}

    #Only return the valid text file format
    Example :
    Job Title
    Title of job

    NO PREAMBLE & Keep everything short, crisp and to the point.
    ''')

    website_chain_extract = website_prompt_extract | llm
    job_description = website_chain_extract.invoke({"website_content": website_content})
    return job_description.content


def get_template(job_description, resume_KTs, llm):
    template_prompt = PromptTemplate.from_template('''
    You are an AI bot designed to act as a professional for creating Cover Letter. You are given with Job Description and Candidate professional details,
    based on these two descriptions give details of the following information from the content:

    1. Asking for Job Opportunity
    2. Why I suits best for this role
    3. My skills relevant to job description 
    4. My past experience relevant to job description
    5. How can I add value to the company
    6. My name, email, phone number with thank note 

    Job description Content:
    {job_description}

    Candidate professional details:
    {resume_KTs}

    #Only return the valid text file format

    Note : Maximum 250 words in the cover letter.
    Note : Not write anything exagerated from candidate professional details.
    Note : Focus on quantitative value to express my projects relevant to job description.
    Note : Don't use bulletins, use 2 paragraph.
    Note : Contact details should be like, in the  very end

    <Name>
    <Email>
    <Phone Number>

    NO PREAMBLE & Keep everything short, crisp and to the point.
    ''')

    template_chain = template_prompt | llm
    cover_letter_template = template_chain.invoke({"job_description": job_description, "resume_KTs": resume_KTs})
    return cover_letter_template.content