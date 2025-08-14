'use client';

import { useState , useEffect} from 'react';
import { getCookie } from '../../utils/getCookie';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isReady, setIsReady] = useState(false);



    useEffect(() => {
    
    const ensureCsrfCookie = async () => {
      try {
      
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/csrf-cookie`, {
            credentials: 'include',
        });
      } catch (err) {
        console.error("Failed to fetch CSRF cookie", err);
        setError("Could not connect to the server. Please try again later.");
      } finally {
        setIsReady(true);
      }

    };
    ensureCsrfCookie();
  }, []); 

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if(!isReady) return;
    setError('');

    const csrfToken = getCookie('csrftoken');

     if (!csrfToken) {
      setError("Could not verify security token. Please refresh the page and try again.");
      return;
    }

    const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/login`;

    const response = await fetch(apiUrl, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' , 'X-CSRFToken': csrfToken,},
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
       window.location.href = '/dashboard';
    } else {
      setError('Invalid username or password.');
    }
  };

  return (
    <main className="flex min-h flex-col items-center justify-center p-24">
      <div className="w-full max-w-md ">
        <form onSubmit={handleSubmit} className="bg-purple-800 shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>
          {error && <p className="bg-red-400 text-white text-center p-2 rounded mb-4">{error}</p>}
          <div className="mb-4">
            <label className="block text-gray-300 text-sm font-bold mb-2" htmlFor="username">
              Username
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 bg-gray-700 text-white leading-tight focus:outline-none focus:shadow-outline"
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-300 text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 bg-gray-700 text-white mb-3 leading-tight focus:outline-none focus:shadow-outline"
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="flex items-center justify-between">
            <button
              className="bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
              type="submit"
            >
              Sign In
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}