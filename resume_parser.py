import spacy
import PyPDF2
import os
import csv

# Load spaCy NLP model
nlp = spacy.load('en_core_web_sm')

def read_resume(file_path):
    return read_pdf(file_path)

def extract_information(resume_text):
    doc = nlp(resume_text)

    skills = [token.text for token in doc if token.pos_ == 'NOUN']
    degrees = [ent.text for ent in doc.ents if ent.label_ == 'DEGREE']
    experience_sentences = [sent.text for sent in doc.sents if 'experience' in sent.text.lower()]

    return skills, degrees, experience_sentences

def filter_resume(resume_text, required_skills, required_degrees, required_experience):
    skills, degrees, experience = extract_information(resume_text)

    meets_criteria = all(skill in skills for skill in required_skills) and \
                     any(degree in degrees for degree in required_degrees) and \
                     any(keyword in ' '.join(experience) for keyword in required_experience)

    return meets_criteria

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        resume_text = ''
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
        return resume_text

# Add your required_skills, required_degrees, and required_experience
required_skills = ['python', 'machine learning', 'data analysis']
required_degrees = ['Bachelor', 'Master']
required_experience = ['5 years', 'senior', 'lead']

# Directory containing multiple resumes in PDF format
resumes_directory = 'D:\\TECHFESTFINALS\\assets'

# CSV file to store results
csv_file_path = 'D:\\TECHFESTFINALS\\results.csv'

# Open CSV file for writing
with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['Name', 'File', 'Meets Criteria']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write header to CSV
    csv_writer.writeheader()

    # Iterate over each resume in the directory
    for resume_file in os.listdir(resumes_directory):
        resume_path = os.path.join(resumes_directory, resume_file)
        resume_text = read_resume(resume_path)

        # Check if the resume meets the criteria
        meets_criteria = filter_resume(resume_text, required_skills, required_degrees, required_experience)

        # Write results to CSV
        csv_writer.writerow({'Name': resume_file, 'File': resume_path, 'Meets Criteria': meets_criteria})

        if meets_criteria:
            print(f"Resume {resume_file} meets the criteria.")
        else:
            print(f"Resume {resume_file} does not meet the criteria.")

print(f"Results written to {csv_file_path}")
