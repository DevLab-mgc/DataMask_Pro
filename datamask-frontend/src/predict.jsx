import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";

function Predict() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!selectedFile) {
      alert("Please select a file to upload");
      return;
    }

    setIsUploading(true);

    try {
      // Simulate file upload and processing
      // In a real application, you would use an API call here
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      navigate('/result', { 
        state: { 
          fileName: selectedFile.name, 
          fileType: selectedFile.type 
        } 
      });
    } catch (error) {
      console.error("File upload failed", error);
      alert("File upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#1e1e1e]">
      <Navbar />
      <div className="text-center flex flex-col gap-4 justify-center items-center h-[calc(100vh-64px)]">
        <h1 className="text-4xl font-semibold mb-4 text-white">Upload a File</h1>
        <form 
          onSubmit={handleSubmit} 
          className="flex flex-col gap-4 w-full max-w-md"
        >
          <div className="w-full">
            <label 
              className="flex h-48 w-full cursor-pointer appearance-none items-center justify-center rounded-md border-2 border-dashed border-gray-600 p-6 transition-all hover:border-gray-400"
            >
              <div className="space-y-1 text-center">
                <div className="mx-auto inline-flex h-10 w-10 items-center justify-center rounded-full bg-gray-100">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    strokeWidth="1.5"
                    stroke="currentColor"
                    className="h-6 w-6 text-gray-900"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z"
                    />
                  </svg>
                </div>
                <div className="text-white">
                  {selectedFile 
                    ? `Selected: ${selectedFile.name}` 
                    : "Click to upload or drag and drop"
                  }
                </div>
                <input 
                  type="file" 
                  className="hidden" 
                  onChange={handleFileChange}
                  accept=".txt,.pdf,.docx,.doc"
                />
                <p className="text-sm text-gray-400">
                  txt, pdf, docx, doc (max 10MB)
                </p>
              </div>
            </label>
          </div>
          <button
            type="submit"
            disabled={!selectedFile || isUploading}
            className="w-full py-2.5 px-5 bg-[#f1f3f5] hover:bg-[#ddd] text-[1.185rem] text-gray-900 font-semibold rounded-full disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isUploading ? "Processing..." : "Upload and Process"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Predict;
