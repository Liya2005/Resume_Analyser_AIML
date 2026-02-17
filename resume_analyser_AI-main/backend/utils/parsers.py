import PyPDF2
from docx import Document
import re

class ResumeParser:
    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def extract_text_from_docx(self, file_path):
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    
    def extract_email(self, text):
        patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'Email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
        ]
        
        for pattern in patterns:
            emails = re.findall(pattern, text, re.IGNORECASE)
            if emails:
                return emails[0] if isinstance(emails[0], str) else emails[0]
        return None
    
    def extract_phone(self, text):
        patterns = [
            r'(?:Phone|Mobile|Tel|Contact)[:\s]*([+]?\d{1,3}[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})',
            r'([+]?\d{1,3}[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})',
            r'([+]?\d{10,15})',
            r'(\d{3}[\s.-]\d{3}[\s.-]\d{4})'
        ]
        
        for pattern in patterns:
            phones = re.findall(pattern, text, re.IGNORECASE)
            if phones:
                phone = phones[0]
                clean_phone = re.sub(r'[^\d+]', '', phone)
                if len(clean_phone) >= 10:
                    return phone
        return None
    
    def extract_skills(self, text):
        common_skills = [
            'Python', 'JavaScript', 'Java', 'React', 'Node.js', 'SQL', 'MongoDB',
            'AWS', 'Docker', 'Kubernetes', 'Git', 'HTML', 'CSS', 'Angular',
            'Vue.js', 'Flask', 'Django', 'Express', 'PostgreSQL', 'MySQL'
        ]
        found_skills = []
        text_lower = text.lower()
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return found_skills
    
    def extract_education(self, text):
        education = []
        
        # Extract CGPA/Percentage patterns
        cgpa_patterns = [
            r'CGPA[:\s]*([0-9]\.[0-9]{1,2})',
            r'GPA[:\s]*([0-9]\.[0-9]{1,2})',
            r'([0-9]\.[0-9]{1,2})[\s]*CGPA',
            r'([0-9]\.[0-9]{1,2})[\s]*/[\s]*([0-9]\.[0-9]{1,2})'
        ]
        
        percentage_patterns = [
            r'([0-9]{1,2}\.[0-9]{1,2})%',
            r'([0-9]{1,2})%',
            r'Percentage[:\s]*([0-9]{1,2}\.[0-9]{1,2})',
            r'([0-9]{1,2}\.[0-9]{1,2})[\s]*percent'
        ]
        
        # Find CGPA
        for pattern in cgpa_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        education.append(f"CGPA: {match[0]}")
                    else:
                        education.append(f"CGPA: {match}")
        
        # Find Percentage
        for pattern in percentage_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                for match in matches:
                    percentage = float(match) if match.replace('.', '').isdigit() else 0
                    if 30 <= percentage <= 100:
                        education.append(f"Percentage: {match}%")
        
        # Extract degree information
        degree_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma', 'b.tech', 'm.tech', 'mba']
        lines = text.split('\n')
        
        for line in lines:
            line_clean = line.strip()
            if len(line_clean) > 10 and any(keyword in line.lower() for keyword in degree_keywords):
                if not any(skip in line.lower() for skip in ['email', 'phone', 'address', 'skill', 'experience', 'work']):
                    if re.search(r'(19|20)\d{2}', line) or any(word in line.lower() for word in ['university', 'college', 'institute']):
                        education.append(line_clean)
        
        return education[:5] if education else ['Education details not clearly specified']