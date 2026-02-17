import re
from datetime import datetime

class ProfileAnalyzer:
    def __init__(self):
        self.skill_weights = {
            'technical': 0.4,
            'experience': 0.3,
            'education': 0.2,
            'completeness': 0.1
        }
    
    def analyze_resume(self, parsed_data):
        scores = {
            'technical_score': self._score_technical_skills(parsed_data.get('skills', [])),
            'experience_score': self._score_experience(parsed_data.get('text', '')),
            'education_score': self._score_education(parsed_data.get('education', [])),
            'completeness_score': self._score_completeness(parsed_data)
        }
        
        overall_score = (
            scores['technical_score'] * self.skill_weights['technical'] +
            scores['experience_score'] * self.skill_weights['experience'] +
            scores['education_score'] * self.skill_weights['education'] +
            scores['completeness_score'] * self.skill_weights['completeness']
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'detailed_scores': scores,
            'recommendations': self._generate_recommendations(scores, parsed_data)
        }
    
    def analyze_linkedin(self, parsed_data):
        # Similar analysis for LinkedIn profiles
        return self.analyze_resume(parsed_data)
    
    def _score_technical_skills(self, skills):
        if not skills:
            return 0
        # Score based on number and relevance of skills
        return min(len(skills) * 10, 100)
    
    def _score_experience(self, text):
        # Count years of experience mentioned
        years_pattern = r'(\d+)\s*(?:years?|yrs?)'
        years = re.findall(years_pattern, text.lower())
        total_years = sum(int(year) for year in years)
        return min(total_years * 10, 100)
    
    def _score_education(self, education):
        if not education:
            return 20
        
        score = 30
        education_text = ' '.join(education).lower()
        
        # Score based on CGPA/Percentage
        cgpa_found = False
        percentage_found = False
        
        # Check for CGPA
        cgpa_matches = re.findall(r'cgpa[:\s]*([0-9]\.[0-9]{1,2})', education_text)
        if cgpa_matches:
            cgpa_found = True
            cgpa_value = float(cgpa_matches[0])
            if cgpa_value >= 9.0:
                score += 25
            elif cgpa_value >= 8.0:
                score += 20
            elif cgpa_value >= 7.0:
                score += 15
            else:
                score += 10
        
        # Check for Percentage
        percentage_matches = re.findall(r'percentage[:\s]*([0-9]{1,2}\.[0-9]{1,2})|([0-9]{1,2})%', education_text)
        if percentage_matches and not cgpa_found:
            percentage_found = True
            for match in percentage_matches:
                percentage = float(match[0] or match[1])
                if percentage >= 85:
                    score += 25
                elif percentage >= 75:
                    score += 20
                elif percentage >= 65:
                    score += 15
                else:
                    score += 10
                break
        
        # Degree level scoring
        if any(word in education_text for word in ['phd', 'doctorate']):
            score += 20
        elif any(word in education_text for word in ['master', 'mba', 'm.tech']):
            score += 15
        elif any(word in education_text for word in ['bachelor', 'b.tech', 'degree']):
            score += 10
        
        # Bonus for having both grades and degree info
        if (cgpa_found or percentage_found) and len(education) > 1:
            score += 10
            
        return min(score, 100)
    
    def _score_completeness(self, data):
        required_fields = ['email', 'phone', 'skills', 'education']
        present_fields = sum(1 for field in required_fields if data.get(field))
        return (present_fields / len(required_fields)) * 100
    
    def _generate_recommendations(self, scores, data):
        recommendations = []
        
        if scores['technical_score'] < 50:
            recommendations.append("Add more technical skills relevant to your field")
        
        if scores['experience_score'] < 50:
            recommendations.append("Highlight more work experience and achievements")
        
        if scores['education_score'] < 50:
            recommendations.append("Include educational background and certifications")
        
        if scores['completeness_score'] < 80:
            recommendations.append("Complete missing contact information")
        
        return recommendations