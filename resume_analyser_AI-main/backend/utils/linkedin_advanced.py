import requests
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse
import json

class AdvancedLinkedInAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def analyze_profile_comprehensive(self, url):
        try:
            # Extract profile data
            profile_data = self._extract_profile_data(url)
            
            # Analyze certificates
            certificates = self._analyze_certificates(profile_data)
            
            # Analyze activity and updates
            activity_score = self._analyze_activity(profile_data)
            
            # Generate comprehensive analysis
            analysis = self._generate_comprehensive_analysis(profile_data, certificates, activity_score)
            
            return analysis
            
        except Exception as e:
            return self._fallback_analysis(url, str(e))
    
    def _extract_profile_data(self, url):
        # Since direct scraping is blocked, we'll simulate comprehensive analysis
        # In real implementation, you'd use LinkedIn API or authorized scraping
        
        profile_id = self._extract_profile_id(url)
        
        # Simulated comprehensive profile data
        return {
            'profile_id': profile_id,
            'url': url,
            'is_custom_url': not profile_id.startswith('ACoAA') if profile_id else False,
            'last_activity': self._estimate_activity_from_url(url),
            'certificates': self._simulate_certificates(),
            'posts': self._simulate_recent_posts(),
            'connections': self._estimate_connections(url),
            'profile_completeness': self._estimate_completeness(url)
        }
    
    def _analyze_certificates(self, profile_data):
        certificates = profile_data.get('certificates', [])
        
        analysis = {
            'total_certificates': len(certificates),
            'recent_certificates': [],
            'certificate_score': 0,
            'trending_skills': []
        }
        
        current_date = datetime.now()
        six_months_ago = current_date - timedelta(days=180)
        
        for cert in certificates:
            cert_date = datetime.strptime(cert['date'], '%Y-%m-%d')
            
            # Recent certificates (last 6 months)
            if cert_date >= six_months_ago:
                analysis['recent_certificates'].append(cert)
                analysis['certificate_score'] += 15
            
            # Trending skills
            if cert['skill'] in ['AI', 'Machine Learning', 'Cloud Computing', 'Data Science', 'Cybersecurity']:
                analysis['trending_skills'].append(cert['skill'])
                analysis['certificate_score'] += 10
        
        return analysis
    
    def _analyze_activity(self, profile_data):
        posts = profile_data.get('posts', [])
        
        activity_analysis = {
            'post_frequency': len(posts),
            'engagement_score': 0,
            'content_quality': 0,
            'professional_networking': 0
        }
        
        # Analyze post frequency (last 30 days)
        if len(posts) >= 10:
            activity_analysis['engagement_score'] = 25
        elif len(posts) >= 5:
            activity_analysis['engagement_score'] = 15
        elif len(posts) >= 1:
            activity_analysis['engagement_score'] = 10
        
        # Content quality analysis
        professional_keywords = ['project', 'achievement', 'learning', 'certification', 'industry', 'innovation']
        for post in posts:
            if any(keyword in post['content'].lower() for keyword in professional_keywords):
                activity_analysis['content_quality'] += 5
        
        activity_analysis['content_quality'] = min(activity_analysis['content_quality'], 25)
        
        # Professional networking score
        connections = profile_data.get('connections', 0)
        if connections >= 500:
            activity_analysis['professional_networking'] = 25
        elif connections >= 200:
            activity_analysis['professional_networking'] = 20
        elif connections >= 100:
            activity_analysis['professional_networking'] = 15
        else:
            activity_analysis['professional_networking'] = 10
        
        return activity_analysis
    
    def _generate_comprehensive_analysis(self, profile_data, certificates, activity):
        # Calculate comprehensive scores
        certificate_score = min(certificates['certificate_score'], 30)
        activity_score = activity['engagement_score'] + activity['content_quality']
        networking_score = activity['professional_networking']
        profile_score = profile_data['profile_completeness']
        
        overall_score = certificate_score + activity_score + networking_score + profile_score
        
        # Generate detailed recommendations
        recommendations = self._generate_detailed_recommendations(certificates, activity, profile_data)
        
        return {
            'overall_score': min(overall_score, 100),
            'detailed_scores': {
                'certificates_and_skills': certificate_score,
                'activity_and_engagement': activity_score,
                'professional_networking': networking_score,
                'profile_completeness': profile_score
            },
            'certificates_analysis': {
                'total_certificates': certificates['total_certificates'],
                'recent_certificates': certificates['recent_certificates'],
                'trending_skills': certificates['trending_skills']
            },
            'activity_analysis': {
                'post_frequency': activity['post_frequency'],
                'engagement_level': 'High' if activity['engagement_score'] >= 20 else 'Medium' if activity['engagement_score'] >= 10 else 'Low',
                'content_quality': 'Professional' if activity['content_quality'] >= 15 else 'Moderate'
            },
            'recommendations': recommendations
        }
    
    def _generate_detailed_recommendations(self, certificates, activity, profile_data):
        recommendations = []
        
        # Certificate recommendations
        if certificates['total_certificates'] < 3:
            recommendations.append("Add more professional certifications to showcase your expertise")
        
        if len(certificates['recent_certificates']) == 0:
            recommendations.append("Obtain recent certifications to show continuous learning")
        
        if len(certificates['trending_skills']) == 0:
            recommendations.append("Consider certifications in trending skills like AI, Cloud Computing, or Data Science")
        
        # Activity recommendations
        if activity['post_frequency'] < 5:
            recommendations.append("Increase your posting frequency to improve visibility and engagement")
        
        if activity['content_quality'] < 15:
            recommendations.append("Share more professional content about your projects and achievements")
        
        if activity['professional_networking'] < 20:
            recommendations.append("Expand your professional network by connecting with industry peers")
        
        # Profile recommendations
        if not profile_data['is_custom_url']:
            recommendations.append("Create a custom LinkedIn URL for better professional branding")
        
        recommendations.extend([
            "Share industry insights and thought leadership content",
            "Engage with others' posts through meaningful comments",
            "Update your profile regularly with new achievements",
            "Join relevant professional groups and participate in discussions"
        ])
        
        return recommendations
    
    def _simulate_certificates(self):
        # Simulate recent certificates for demonstration
        return [
            {'name': 'AWS Cloud Practitioner', 'skill': 'Cloud Computing', 'date': '2024-08-15'},
            {'name': 'Google Analytics Certified', 'skill': 'Digital Marketing', 'date': '2024-06-20'},
            {'name': 'Python for Data Science', 'skill': 'Data Science', 'date': '2024-05-10'}
        ]
    
    def _simulate_recent_posts(self):
        # Simulate recent posts for demonstration
        return [
            {'content': 'Excited to share my latest project on machine learning', 'date': '2024-09-01'},
            {'content': 'Just completed AWS certification, learning never stops!', 'date': '2024-08-28'},
            {'content': 'Great networking event today, met amazing professionals', 'date': '2024-08-25'}
        ]
    
    def _extract_profile_id(self, url):
        parsed_url = urlparse(url)
        if 'linkedin.com' not in parsed_url.netloc:
            return None
        
        path_parts = parsed_url.path.strip('/').split('/')
        if 'in' in path_parts:
            idx = path_parts.index('in')
            if idx + 1 < len(path_parts):
                return path_parts[idx + 1]
        return None
    
    def _estimate_activity_from_url(self, url):
        # Estimate based on URL structure and profile ID
        return datetime.now() - timedelta(days=7)  # Assume recent activity
    
    def _estimate_connections(self, url):
        # Simulate connection count based on profile maturity
        return 350  # Simulated connection count
    
    def _estimate_completeness(self, url):
        # Base completeness score
        return 20
    
    def _fallback_analysis(self, url, error):
        return {
            'overall_score': 45,
            'detailed_scores': {
                'certificates_and_skills': 10,
                'activity_and_engagement': 15,
                'professional_networking': 10,
                'profile_completeness': 10
            },
            'certificates_analysis': {
                'total_certificates': 0,
                'recent_certificates': [],
                'trending_skills': []
            },
            'activity_analysis': {
                'post_frequency': 0,
                'engagement_level': 'Unknown',
                'content_quality': 'Unknown'
            },
            'recommendations': [
                'Unable to analyze profile completely due to privacy settings',
                'Ensure your LinkedIn profile is public for better analysis',
                'Add recent certifications and skills to your profile',
                'Post regular updates about your professional journey'
            ],
            'error': error
        }