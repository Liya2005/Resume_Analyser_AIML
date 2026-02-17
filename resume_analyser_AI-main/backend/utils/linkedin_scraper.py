import re
import requests
from urllib.parse import urlparse

class LinkedInAnalyzer:
    def analyze_profile_url(self, url):
        # Extract profile information from URL
        profile_data = self._extract_profile_info(url)
        
        # Since direct scraping is blocked, we'll analyze based on URL structure
        # and provide general recommendations
        return {
            'profile_url': url,
            'profile_id': profile_data.get('profile_id'),
            'is_custom_url': profile_data.get('is_custom_url'),
            'recommendations': self._generate_url_recommendations(profile_data)
        }
    
    def _extract_profile_info(self, url):
        # Parse LinkedIn URL to extract profile information
        parsed_url = urlparse(url)
        
        if 'linkedin.com' not in parsed_url.netloc:
            raise ValueError("Invalid LinkedIn URL")
        
        # Extract profile ID or custom URL
        path_parts = parsed_url.path.strip('/').split('/')
        
        if 'in' in path_parts:
            idx = path_parts.index('in')
            if idx + 1 < len(path_parts):
                profile_id = path_parts[idx + 1]
                is_custom_url = not profile_id.startswith('ACoAA')
                return {
                    'profile_id': profile_id,
                    'is_custom_url': is_custom_url,
                    'valid': True
                }
        
        return {'valid': False}
    
    def _generate_url_recommendations(self, profile_data):
        recommendations = []
        
        if not profile_data.get('valid'):
            recommendations.append("Invalid LinkedIn URL provided")
            return recommendations
        
        if not profile_data.get('is_custom_url'):
            recommendations.append("Create a custom LinkedIn URL for better professional branding")
        
        recommendations.extend([
            "Ensure your LinkedIn profile is public for better visibility",
            "Add a professional profile photo",
            "Write a compelling headline and summary",
            "List your skills and get endorsements",
            "Add work experience with detailed descriptions",
            "Include education and certifications",
            "Get recommendations from colleagues",
            "Post regular updates and articles"
        ])
        
        return recommendations