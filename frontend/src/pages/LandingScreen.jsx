import React from 'react'
import { useNavigate } from 'react-router-dom';

import '../styles/LandingScreen.css';
import trybutton from '../assets/buttons/TryItNowButton.png';

export const LandingScreen = () => {
  const navigate = useNavigate(); // navigation

  const handleNavigate = () => {
    navigate('/prompt');
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      console.log('📄 Uploaded PDF:', file);
      // TODO: Save file to state or pass to another screen
    } else {
      alert('Please upload a valid PDF file');
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
        onClick={handleNavigate}
      />

      <div className="upload-container">
        <input
          type="file"
          id="pdf-upload"
          accept="application/pdf"
          onChange={handleFileUpload}
        />
      </div>
    </div>
  );
};
