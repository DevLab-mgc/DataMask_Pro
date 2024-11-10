import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FcGoogle } from "react-icons/fc";
import logo from '/src/assets/deeptrace_logo_transparent.png';
import { loginUser } from '../../APIs/userDetails';

function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await loginUser(formData);
      navigate('/predict');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='h-screen flex justify-center items-center gap-36 bg-[#1e1e1e]'>
      <div className='flex gap-[30px]'>
        <img src={logo} alt="DeepTrace Logo" className='h-16' />
        <div className='text-5xl font-bold text-white'>DeepTrace</div>
      </div>
      <div className='bg-[#252525] px-12 py-16 rounded-[20px]'>
        <div>
          <div className='text-sm font-semibold text-[#787878]'>Log In</div>
          <div className='text-3xl font-semibold text-white'>Welcome Back!</div>
        </div>

        <div className='mt-8'>
          <div className='text-md text-white'>
            New User? <a href='/signup' className='text-[#1473E6] hover:text-[#2484f7]'>Sign Up</a>
          </div>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-500 bg-opacity-10 border border-red-500 rounded-lg text-red-500">
            {error}
          </div>
        )}

        <div className='mt-8'>
          <button 
            onClick={() => {
              window.location.href = "http://localhost:8000/auth/google";
            }} 
            className='w-[360px] flex gap-4 justify-center items-center px-4 py-2.5 rounded-full border border-1 border-[#f1f3f515] text-white hover:bg-[#f1f3f505]'
          >
            <FcGoogle className='scale-[1.5]'/> Log In with Google
          </button>
        </div>

        <div className="mt-1">
          <div className="inline-flex items-center justify-center w-full">
            <hr className="w-full h-px my-8 bg-[#f1f3f515] border-0" />
            <span className="absolute px-3 font-medium text-[#f1f3f550] bg-[#252525]">
              Or
            </span>
          </div>
        </div>

        <div className="mt-1">
          <form onSubmit={handleSubmit} className="flex flex-col gap-1.5">
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Email Address"
              required
              className="w-[360px] px-4 py-2.5 bg-[#1e1e1e] text-white rounded-full border border-1 border-[#f1f3f515] hover:border hover:border-[#f1f3f550] focus:outline-none focus:border-[#1473E6]"
            />
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Password"
              required
              className="w-[360px] px-4 py-2.5 bg-[#1e1e1e] text-white rounded-full border border-1 border-[#f1f3f515] hover:border hover:border-[#f1f3f550] focus:outline-none focus:border-[#1473E6]"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="w-[360px] px-4 py-2.5 rounded-full bg-[#f1f3f5] hover:bg-[#ddd] text-md text-gray-900 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Logging in...' : 'Log In'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
