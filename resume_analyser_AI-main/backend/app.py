from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from models.simple_storage import SimpleStorage
from utils.parsers import ResumeParser
from services.analyzer import ProfileAnalyzer
from utils.linkedin_advanced import AdvancedLinkedInAnalyzer

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SimpleStorage()
parser = ResumeParser()
analyzer = ProfileAnalyzer()
linkedin_analyzer = AdvancedLinkedInAnalyzer()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Resume Analyzer API is running', 'endpoints': ['/api/upload-resume', '/api/analyze-linkedin-url', '/api/analyses']})

@app.route('/api', methods=['GET'])
def api_info():
    return jsonify({'message': 'Resume Analyzer API', 'version': '1.0'})

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = parser.extract_text_from_pdf(filepath)
        else:
            text = parser.extract_text_from_docx(filepath)
        
        # Parse candidate details
        parsed_data = {
            'text': text,
            'email': parser.extract_email(text),
            'phone': parser.extract_phone(text),
            'skills': parser.extract_skills(text),
            'education': parser.extract_education(text),
            'type': 'resume'
        }
        
        # Analyze and score
        analysis = analyzer.analyze_resume(parsed_data)
        
        # Save to database
        result = {
            'parsed_data': parsed_data,
            'analysis': analysis,
            'filename': filename
        }
        
        db_result = db.save_analysis(result)
        result['_id'] = db_result.inserted_id
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/api/analyze-linkedin-url', methods=['POST'])
def analyze_linkedin_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'LinkedIn URL is required'}), 400
    
    url = data['url'].strip()
    
    try:
        # Comprehensive LinkedIn analysis
        linkedin_analysis = linkedin_analyzer.analyze_profile_comprehensive(url)
        
        analysis = linkedin_analysis
        
        result = {
            'parsed_data': {
                'profile_url': url,
                'certificates': linkedin_analysis.get('certificates_analysis', {}),
                'activity': linkedin_analysis.get('activity_analysis', {}),
                'type': 'linkedin_url'
            },
            'analysis': analysis,
            'url': url
        }
        
        db_result = db.save_analysis(result)
        result['_id'] = db_result.inserted_id
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyses', methods=['GET'])
def get_analyses():
    analyses = db.get_all_analyses()
    return jsonify(analyses)

@app.route('/api/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    analysis = db.get_analysis(analysis_id)
    if analysis:
        return jsonify(analysis)
    return jsonify({'error': 'Analysis not found'}), 404

if __name__ == '__main__':
    print('Starting Resume Analyzer API on http://localhost:5000')
    print('Available endpoints:')
    print('  GET  / - API info')
    print('  POST /api/upload-resume - Upload resume')
    print('  POST /api/analyze-linkedin-url - Analyze LinkedIn profile URL')
    print('  GET  /api/analyses - Get all analyses')
    app.run(debug=True, port=5000, host='0.0.0.0')