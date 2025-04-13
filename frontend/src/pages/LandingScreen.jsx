import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import '../styles/LandingScreen.css';
import trybutton from '../assets/buttons/TryItNowButton.png';

export const LandingScreen = () => {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setUploadStatus('');
    } else {
      alert('Please upload a valid PDF file');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/question', { //change depending on backend
        method: 'POST',
        body: formData,
      });

      if (response.ok) { 
        setUploadStatus('File uploaded successfully!');
        navigate('/prompt');
      } else {
        setUploadStatus('Upload failed.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('An error occurred during upload.');
    }
  };

  return (
    <div className="landing-screen">
      <h1 className="landing-screen-title">
        Why Study Alone?
        <br />
        Let Your Favorite Characters Tutor You!
      </h1>

      <p className="landing-subheading">
        Please help me study
        <br />
        with real-time tutoring
        <br />
        that actually helps me learn!
      </p>

      <img
        className="try-button"
        src={trybutton}
        alt="Try It Now Button"
        onClick={handleUpload}
      />

      <div className="upload-container">
        <input
          type="file"
          id="pdf-upload"
          accept="application/pdf"
          onChange={handleFileChange}
        />
        <p>{uploadStatus}</p>
      </div>
    </div>
  );
};
