import re
import fitz# PyMuPDF

def clean_text(text):
    text = re.sub(r"\n(?=\w)", " ", text)
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\xa0", "", text)
    return text

def pdf_extractor(file):
    # Ensure the uploaded file is read as a byte stream
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# def deepseek_cleaning(cover_letter):
#     cover_letter = cover_letter.split('</think>')[1]
#     return cover_letter