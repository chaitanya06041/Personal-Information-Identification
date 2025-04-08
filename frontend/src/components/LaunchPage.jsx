import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LaunchPage.css";

const LaunchPage = () => {
  const navigate = useNavigate();
  const [show, setShow] = useState(false);

  useEffect(() => {
    setTimeout(() => setShow(true), 100);
  }, []);

  return (
    <div className={`launch-container ${show ? "animate" : ""}`}>
      <div className="animated-bg">
        <div className="waves"></div>
        <div className="blob pink"></div>
        <div className="blob blue"></div>
      </div>

      <div className="hero">
        <h1 className="fade-up delay-1">Protect What Matters</h1>
        <p className="fade-up delay-2">AI-powered PII Detection & Masking</p>
        <button className="fade-up delay-3" onClick={() => navigate("/mask")}>
          Start Masking
        </button>
      </div>

      <div className="features">
        <div className="card fade-up delay-4">
          <h2>🔍 What It Does</h2>
          <p>Scans images & PDFs.</p>
          <p>Detects sensitive info.</p>
          <p>Masks them automatically.</p>
        </div>
        <div className="card fade-up delay-5">
          <h2>🧠 How It Works</h2>
          <p>OCR + preprocessing.</p>
          <p>AI extracts key data.</p>
          <p>Output is privacy-safe.</p>
        </div>
        <div className="card fade-up delay-6">
          <h2>🔐 Why It Matters</h2>
          <p>Prevent leaks.</p>
          <p>Comply with privacy laws.</p>
          <p>Secure user data.</p>
        </div>
      </div>

      <div className="footer fade-up delay-7">
        <h3>Built for devs, businesses & privacy advocates.</h3>
        <p>Try it now — no setup required.</p>
        <button onClick={() => navigate("/mask")}>Go to Masking Tool ➜</button>
      </div>
    </div>
  );
};

export default LaunchPage;
