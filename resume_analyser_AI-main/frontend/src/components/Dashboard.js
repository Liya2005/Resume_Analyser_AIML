import React from 'react';

const Dashboard = ({ analysis }) => {
  if (!analysis) return null;

  const { parsed_data, analysis: scores } = analysis;

  const ScoreCard = ({ title, score, color }) => (
    <div className="score-card">
      <h3>{title}</h3>
      <div className="score-circle" style={{ borderColor: color }}>
        <span className="score-number">{score}</span>
      </div>
    </div>
  );

  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FF9800';
    return '#F44336';
  };

  return (
    <div className="dashboard">
      <div className="analysis-header">
        <h2 className="analysis-title">Your Professional Analysis</h2>
        <span className="file-type">
          {parsed_data.type === 'resume' ? '📄 Resume' : '🔗 LinkedIn'} Analysis
        </span>
      </div>

      <div className="overall-score">
        <ScoreCard 
          title="🏆 Overall Score" 
          score={scores.overall_score} 
          color={getScoreColor(scores.overall_score)}
        />
      </div>

      <div className="detailed-scores">
        <ScoreCard 
          title="💻 Technical Skills" 
          score={Math.round(scores.detailed_scores.technical_score || scores.detailed_scores.profile_completeness || 0)} 
          color={getScoreColor(scores.detailed_scores.technical_score || scores.detailed_scores.profile_completeness || 0)}
        />
        <ScoreCard 
          title="💼 Experience" 
          score={Math.round(scores.detailed_scores.experience_score || scores.detailed_scores.url_optimization || 0)} 
          color={getScoreColor(scores.detailed_scores.experience_score || scores.detailed_scores.url_optimization || 0)}
        />
        <ScoreCard 
          title="🎓 Education" 
          score={Math.round(scores.detailed_scores.education_score || scores.detailed_scores.accessibility || 0)} 
          color={getScoreColor(scores.detailed_scores.education_score || scores.detailed_scores.accessibility || 0)}
        />
        <ScoreCard 
          title="✓ Completeness" 
          score={Math.round(scores.detailed_scores.completeness_score || scores.detailed_scores.professional_branding || 0)} 
          color={getScoreColor(scores.detailed_scores.completeness_score || scores.detailed_scores.professional_branding || 0)}
        />
      </div>

      <div className="parsed-info">
        {parsed_data.type === 'resume' ? (
          <>
            <div className="info-section">
              <h3>📧 Contact Information</h3>
              <p>Email: {parsed_data.email || 'Not found'}</p>
              <p>Phone: {parsed_data.phone || 'Not found'}</p>
            </div>

            <div className="info-section">
              <h3>🛠️ Skills Found ({parsed_data.skills?.length || 0})</h3>
              <div className="skills-list">
                {parsed_data.skills?.map((skill, index) => (
                  <span key={index} className="skill-tag">{skill}</span>
                )) || <p>No skills detected</p>}
              </div>
            </div>

            <div className="info-section">
              <h3>🎓 Education</h3>
              {parsed_data.education?.length ? (
                <ul>
                  {parsed_data.education.map((edu, index) => (
                    <li key={index}>{edu}</li>
                  ))}
                </ul>
              ) : <p>No education information found</p>}
            </div>
          </>
        ) : (
          <>
            <div className="info-section">
              <h3>🏆 Recent Certificates</h3>
              {parsed_data.certificates?.recent_certificates?.length ? (
                <ul>
                  {parsed_data.certificates.recent_certificates.map((cert, index) => (
                    <li key={index}>
                      <strong>{cert.name}</strong> - {cert.skill} ({cert.date})
                    </li>
                  ))}
                </ul>
              ) : <p>No recent certificates found</p>}
              <p>Total Certificates: {parsed_data.certificates?.total_certificates || 0}</p>
            </div>

            <div className="info-section">
              <h3>📈 Activity Analysis</h3>
              <p>Post Frequency: {parsed_data.activity?.post_frequency || 0} posts (last 30 days)</p>
              <p>Engagement Level: {parsed_data.activity?.engagement_level || 'Unknown'}</p>
              <p>Content Quality: {parsed_data.activity?.content_quality || 'Unknown'}</p>
            </div>

            <div className="info-section">
              <h3>🔥 Trending Skills</h3>
              <div className="skills-list">
                {parsed_data.certificates?.trending_skills?.map((skill, index) => (
                  <span key={index} className="skill-tag">{skill}</span>
                )) || <p>No trending skills identified</p>}
              </div>
            </div>
          </>
        )}
      </div>

      <div className="recommendations">
        <h3>💡 Personalized Recommendations</h3>
        {scores.recommendations?.length ? (
          <ul>
            {scores.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        ) : <p>🎉 Excellent! Your profile looks great. Keep up the good work!</p>}
      </div>
    </div>
  );
};

export default Dashboard;