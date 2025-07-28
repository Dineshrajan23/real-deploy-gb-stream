'use client';

import { useState, useEffect } from 'react'; 
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { getCookie } from '../../utils/getCookie'; 

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isReady, setIsReady] = useState(false); 
  const router = useRouter();


  useEffect(() => {
    const ensureCsrfCookie = async () => {
      try {
        await fetch('/api/csrf-cookie', { credentials: 'include' });
      } catch (err) {
        console.error("Failed to fetch CSRF cookie", err);
      } finally {
        setIsReady(true);
      }
    };
    ensureCsrfCookie();
  }, []);
  

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

  
    const csrfToken = getCookie('csrftoken');
    if (!csrfToken) {
      setError("Security token not found. Please refresh and try again.");
      return;
    }

    const response = await fetch('/api/register', {
      method: 'POST',
      credentials: 'include', 
      headers: { 
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken, 
      },
      body: JSON.stringify({ username, email, password }),
    });
    

    const data = await response.json();

    if (response.ok) {
      alert('Registration successful! Please log in.');
      router.push('/login');
    } else {
      setError(data.detail || 'Registration failed.');
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md">
        <form onSubmit={handleSubmit} className="bg-gray-800 shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h1 className="text-2xl font-bold mb-6 text-center">Create Account</h1>
          {error && <p className="bg-red-500 text-white text-center p-2 rounded mb-4">{error}</p>}
          
          <div className="mb-4">
            <label className="block text-gray-300 text-sm font-bold mb-2" htmlFor="username">Username</label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 bg-gray-700 text-white" id="username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} required suppressHydrationWarning={true} />
          </div>

          <div className="mb-4">
            <label className="block text-gray-300 text-sm font-bold mb-2" htmlFor="email">Email</label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 bg-gray-700 text-white" id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required suppressHydrationWarning={true} />
          </div>

          <div className="mb-6">
            <label className="block text-gray-300 text-sm font-bold mb-2" htmlFor="password">Password</label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 bg-gray-700 text-white" id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required suppressHydrationWarning={true} />
          </div>

          <div className="flex flex-col items-center justify-between">
            <button 
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full disabled:bg-gray-500" 
              type="submit"
              disabled={!isReady} 
            >
              {isReady ? 'Sign Up' : 'Connecting...'}
            </button>
            <Link href="/login" className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800 mt-4">
              Already have an account?
            </Link>
          </div>
        </form>
      </div>
    </main>
  );
}