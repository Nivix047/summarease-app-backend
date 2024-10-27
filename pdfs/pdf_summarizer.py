import nltk
import PyPDF2
import openai
import os
from collections import deque
from sacremoses import MosesDetokenizer
from dotenv import load_dotenv

# Load OpenAI API key from environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure the 'punkt' tokenizer models are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file_obj:
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page_obj = pdf_reader.pages[page_num]
                text += page_obj.extract_text() or ""
        if not text:
            print("Warning: No text was extracted from the PDF.")
        else:
            print(f"Extracted text: {text[:1000]}")  # Print the first 1000 characters
        return text.strip()
    except Exception as e:
        print(f"An error occurred while extracting text from the PDF: {str(e)}")
        return None

def gpt_summarize(text):
    try:
        print(f"Summarizing text: {text[:500]}")  # Print the first 500 characters of the text being summarized
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a summarizing application."},
                {"role": "user", "content": f"{text}\n\nSummarize:"},
            ]
        )
        print(f"Response: {response}")  # Print the response
        return response
    except Exception as e:
        print(f"An error occurred during summarization: {str(e)}")
        return None

def recursively_summarize(text, section_size=3000, overlap=150):
    detokenizer = MosesDetokenizer()

    # Ensure the 'punkt' tokenizer models are available within this function
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    tokens = nltk.word_tokenize(text)
    summaries = []

    sections = deque()
    start = 0
    while start < len(tokens):
        sections.append(tokens[start:start + section_size])
        start += section_size - overlap
    
    while len(sections) > 0:
        section = sections.popleft()
        summary = gpt_summarize(detokenizer.detokenize(section))
        if summary and 'choices' in summary and summary['choices']:
            summaries.append(summary['choices'][0]['message']['content'])
        else:
            print("Error: Summarization failed.")
            return None
    
    return " ".join(summaries) if summaries else None
