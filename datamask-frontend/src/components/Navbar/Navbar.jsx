import React from 'react';
import { Link } from 'react-router-dom';
import logo from '/src/assets/deeptrace_logo_transparent.png';
import { Upload, Home } from 'lucide-react';

function Navbar() {
  return (
    <nav className="bg-[#252525] p-4 flex justify-between items-center">
      <div className="flex items-center gap-4">
        <img src={logo} alt="DataMask Logo" className="h-10" />
        <span className="text-white text-xl font-bold">DataMask</span>
      </div>

      <div className="flex items-center gap-6">
        <Link 
          to="/home" 
          className="text-white hover:text-[#1473E6] flex items-center gap-2 transition-colors"
        >
          <Home size={20} /> Home
        </Link>
        <Link 
          to="/predict" 
          className="text-white hover:text-[#1473E6] flex items-center gap-2 transition-colors"
        >
          <Upload size={20} /> Predict
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
