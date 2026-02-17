# Resume & LinkedIn Profile Analyzer

A full-stack application that analyzes resumes and LinkedIn profiles, providing scores and recommendations for improvement.

## Features

- **Resume Analysis**: Upload PDF/DOCX resumes for parsing and scoring
- **LinkedIn Analysis**: Upload LinkedIn PDF exports for profile evaluation
- **Scoring System**: 0-100 scoring across technical skills, experience, education, and completeness
- **Recommendations**: Actionable suggestions for profile improvement
- **MongoDB Storage**: Persistent storage of analysis results

## Architecture

- **Backend**: Flask API with MongoDB
- **Frontend**: React.js with drag-and-drop file upload
- **Parsing**: PyPDF2 and python-docx for text extraction
- **Analysis**: Custom scoring algorithms with NLP

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start MongoDB (ensure MongoDB is running locally)

4. Run Flask application:
```bash
python app.py
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start React development server:
```bash
npm start
```

## API Endpoints

- `POST /api/upload-resume` - Upload and analyze resume
- `POST /api/upload-linkedin` - Upload and analyze LinkedIn profile
- `GET /api/analyses` - Get all analysis results
- `GET /api/analysis/<id>` - Get specific analysis result

## MongoDB Schema

```javascript
{
  _id: ObjectId,
  parsed_data: {
    text: String,
    email: String,
    phone: String,
    skills: [String],
    education: [String],
    type: String // 'resume' or 'linkedin'
  },
  analysis: {
    overall_score: Number,
    detailed_scores: {
      technical_score: Number,
      experience_score: Number,
      education_score: Number,
      completeness_score: Number
    },
    recommendations: [String]
  },
  filename: String,
  created_at: Date
}
```

## Usage

1. Open the application in your browser (http://localhost:3000)
2. Select either "Resume" or "LinkedIn Profile" tab
3. Drag and drop your file or click to select
4. View the analysis results with scores and recommendations
5. Click "New Analysis" to analyze another file