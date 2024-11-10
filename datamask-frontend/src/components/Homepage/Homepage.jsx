import React from 'react';
import Navbar from '../Navbar/Navbar';
import { Link } from 'react-router-dom';
import { Upload, FileText, Shield } from 'lucide-react';

function Homepage() {
  return (
    <div className="min-h-screen bg-[#1e1e1e] text-white">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-6">Welcome to DataMask</h1>
          <p className="text-xl text-gray-300 mb-12">
            Protect your sensitive information with advanced PII detection
          </p>

          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-[#252525] p-6 rounded-lg shadow-lg hover:scale-105 transition-transform">
              <Upload className="mx-auto mb-4 text-blue-500" size={48} />
              <h2 className="text-2xl font-semibold mb-4">Upload Files</h2>
              <p className="text-gray-400 mb-4">
                Easily upload documents for PII detection
              </p>
              <Link 
                to="/predict" 
                className="block w-full py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors text-center"
              >
                Start Scanning
              </Link>
            </div>

            <div className="bg-[#252525] p-6 rounded-lg shadow-lg hover:scale-105 transition-transform">
              <FileText className="mx-auto mb-4 text-green-500" size={48} />
              <h2 className="text-2xl font-semibold mb-4">Analyze Documents</h2>
              <p className="text-gray-400 mb-4">
                Detect and identify sensitive personal information
              </p>
              <Link 
                to="/predict" 
                className="block w-full py-2 bg-green-600 text-white rounded-full hover:bg-green-700 transition-colors text-center"
              >
                Analyze Now
              </Link>
            </div>

            <div className="bg-[#252525] p-6 rounded-lg shadow-lg hover:scale-105 transition-transform">
              <Shield className="mx-auto mb-4 text-red-500" size={48} />
              <h2 className="text-2xl font-semibold mb-4">Data Protection</h2>
              <p className="text-gray-400 mb-4">
                Safeguard sensitive information across your documents
              </p>
              <Link 
                to="/predict" 
                className="block w-full py-2 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors text-center"
              >
                Protect Data
              </Link>
            </div>
          </div>

          <div className="mt-16 max-w-2xl mx-auto">
            <h3 className="text-3xl font-bold mb-6">How It Works</h3>
            <div className="bg-[#252525] p-8 rounded-lg">
              <ol className="list-decimal list-inside text-left space-y-4 text-gray-300">
                <li>Upload your document</li>
                <li>Our AI scans for personally identifiable information</li>
                <li>Receive a detailed report of detected PII</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Homepage;
