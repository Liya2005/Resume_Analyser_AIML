import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadResume, analyzeLinkedInUrl } from '../services/api';

const FileUpload = ({ onAnalysisComplete }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadType, setUploadType] = useState('resume');
  const [linkedinUrl, setLinkedinUrl] = useState('');

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploading(true);
    try {
      const response = await uploadResume(file);
      onAnalysisComplete(response.data);
    } catch (error) {
      alert('Upload failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setUploading(false);
    }
  };

  const handleLinkedInAnalysis = async () => {
    if (!linkedinUrl.trim()) {
      alert('Please enter a LinkedIn URL');
      return;
    }

    setUploading(true);
    try {
      const response = await analyzeLinkedInUrl(linkedinUrl);
      onAnalysisComplete(response.data);
    } catch (error) {
      alert('Analysis failed: ' + (error.response?.data?.error || error.message));
    } finally {
      setUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'] },
    multiple: false
  });

  return (
    <div className="upload-container">
      <h2 className="upload-title">Get Your Professional Analysis</h2>
      <p className="upload-subtitle">Upload your resume or analyze your LinkedIn profile to get personalized insights</p>
      
      <div className="upload-type-selector">
        <button 
          className={uploadType === 'resume' ? 'active' : ''}
          onClick={() => setUploadType('resume')}
        >
          📄 Resume Analysis
        </button>
        <button 
          className={uploadType === 'linkedin' ? 'active' : ''}
          onClick={() => setUploadType('linkedin')}
        >
          🔗 LinkedIn Profile
        </button>
      </div>
      
      {uploadType === 'resume' ? (
        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          <div className="dropzone-content">
            {uploading ? (
              <div>
                <div className="upload-icon">⏳</div>
                <p>Analyzing your resume...</p>
                <p className="file-types">This may take a few moments</p>
              </div>
            ) : (
              <div>
                <div className="upload-icon">📁</div>
                <p>Drop your resume here or click to browse</p>
                <p className="file-types">Supports PDF and DOCX files up to 10MB</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="linkedin-url-input">
          <div className="url-input-container">
            <input
              type="url"
              placeholder="https://linkedin.com/in/your-profile"
              value={linkedinUrl}
              onChange={(e) => setLinkedinUrl(e.target.value)}
              className="url-input"
            />
          </div>
          <button 
            onClick={handleLinkedInAnalysis}
            disabled={uploading || !linkedinUrl.trim()}
            className="analyze-btn"
          >
            {uploading ? (
              <>⏳ Analyzing...</>
            ) : (
              <>🔍 Analyze LinkedIn Profile</>
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;