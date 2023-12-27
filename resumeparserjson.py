import spacy
import PyPDF2
import os
import json

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

    # Calculate the percentage of required skills present in the resume
    total_skills = len(required_skills)
    matched_skills = sum(skill in skills for skill in required_skills)
    skills_percentage = (matched_skills / total_skills) * 100 if total_skills > 0 else 0

    # Check if the resume meets the specified criteria
    meets_criteria = all(skill in skills for skill in required_skills) and \
                     any(degree in degrees for degree in required_degrees) and \
                     any(keyword in ' '.join(experience) for keyword in required_experience)

    return meets_criteria, skills_percentage

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

# JSON file to store results
json_file_path = 'D:\\TECHFESTFINALS\\results.json'

# Results dictionary
results = {'resumes': []}

# Iterate over each resume in the directory
for resume_file in os.listdir(resumes_directory):
    resume_path = os.path.join(resumes_directory, resume_file)
    resume_text = read_resume(resume_path)

    # Check if the resume meets the criteria and get skills percentage
    meets_criteria, skills_percentage = filter_resume(resume_text, required_skills, required_degrees, required_experience)

    # Store results in the dictionary
    result_entry = {
        'name': resume_file,
        'file': resume_path,
        'meets_criteria': meets_criteria,
        'skills_percentage': skills_percentage,
        'skills': extract_information(resume_text)[0],
        'degrees': extract_information(resume_text)[1],
        'experience': extract_information(resume_text)[2],
    }

    results['resumes'].append(result_entry)

# Write results to JSON file with indentation for readability
with open(json_file_path, 'w') as json_file:
    json.dump(results, json_file, indent=2)

print(f"Results written to {json_file_path}")
