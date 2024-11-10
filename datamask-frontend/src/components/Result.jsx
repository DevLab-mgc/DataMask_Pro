import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Navbar from "./Navbar/Navbar";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const { fileName, fileType } = location.state || {};

  // Simulated processing results
  const processingResults = {
    piiDetected: [
      { type: 'Email', value: 'user@example.com', line: 5 },
      { type: 'Phone Number', value: '(123) 456-7890', line: 12 }
    ],
    totalPiiCount: 2,
    processingTime: '0.5 seconds'
  };

  const handleBackToUpload = () => {
    navigate('/predict');
  };

  return (
    <div className="min-h-screen bg-[#1e1e1e]">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <div className="bg-[#252525] rounded-lg shadow-lg p-6">
          <h1 className="text-3xl font-bold text-white mb-6">PII Detection Results</h1>
          
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-white mb-2">File Details</h2>
            <div className="bg-[#1e1e1e] p-4 rounded-md">
              <p className="text-gray-300">
                <strong>File Name:</strong> {fileName || 'Unknown File'}
              </p>
              <p className="text-gray-300">
                <strong>File Type:</strong> {fileType || 'Unknown Type'}
              </p>
              <p className="text-gray-300">
                <strong>Processing Time:</strong> {processingResults.processingTime}
              </p>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-white mb-2">PII Detections</h2>
            {processingResults.totalPiiCount > 0 ? (
              <div className="space-y-4">
                {processingResults.piiDetected.map((detection, index) => (
                  <div 
                    key={index} 
                    className="bg-[#1e1e1e] p-4 rounded-md border border-red-500 border-opacity-50"
                  >
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-red-500 font-bold">{detection.type}</span>
                      <span className="text-gray-400">Line {detection.line}</span>
                    </div>
                    <p className="text-white">{detection.value}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-[#1e1e1e] p-4 rounded-md text-green-500">
                No Personally Identifiable Information (PII) detected
              </div>
            )}
          </div>

          <div className="mt-6 flex justify-center">
            <button
              onClick={handleBackToUpload}
              className="px-6 py-2 bg-[#f1f3f5] text-gray-900 rounded-full hover:bg-[#ddd] transition-colors"
            >
              Upload Another File
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Result;
