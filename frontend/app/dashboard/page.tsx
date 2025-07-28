'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

type DashboardData = {
  stream_key: string;
  stream_title: string | null;
  is_live: boolean;
};

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [newTitle, setNewTitle] = useState('');
  const [showKey, setShowKey] = useState(false);
  const router = useRouter();

  const fetchDashboardData = async () => {
    const response = await fetch('/api/dashboard');
    if (response.status === 401) {
      router.push('/login'); 
      return;
    }
    const result = await response.json();
    setData(result);
    setNewTitle(result.stream_title || '');
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleUpdateTitle = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch('/api/dashboard', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTitle }),
    });
    alert('Title updated!');
    fetchDashboardData(); 
  };

  const handleResetKey = async () => {
    if (confirm('Are you sure you want to reset your stream key? This cannot be undone.')) {
      await fetch('/api/dashboard/reset-key', { method: 'POST' });
      alert('Stream key has been reset.');
      fetchDashboardData(); 
    }
  };

  if (!data) {
    return <main className="p-24"><p>Loading dashboard...</p></main>;
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <h1 className="text-4xl font-bold mb-10">My Dashboard</h1>
      <div className="w-full max-w-2xl space-y-8">
        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">Streaming Setup</h2>
          <p className="mb-2"><strong>RTMP Server:</strong> <code>rtmp://localhost:1935/live</code></p>
          <div className="mb-4">
            <p className="mb-2"><strong>Stream Key:</strong></p>
            <div className="flex items-center space-x-4 bg-gray-900 p-2 rounded">
              <input
                type={showKey ? 'text' : 'password'}
                readOnly
                value={data.stream_key}
                className="bg-transparent text-white font-mono w-full"
              />
              <button onClick={() => setShowKey(!showKey)} className="text-sm text-blue-400 hover:text-blue-300">
                {showKey ? 'Hide' : 'Show'}
              </button>
            </div>
          </div>
          <button onClick={handleResetKey} className="text-sm text-red-500 hover:text-red-400">
            Reset Key
          </button>
        </div>

       
        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-2xl font-semibold mb-4">Stream Details</h2>
          <form onSubmit={handleUpdateTitle}>
            <label htmlFor="title" className="block text-sm font-medium text-gray-300 mb-2">Stream Title</label>
            <input
              id="title"
              type="text"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              className="w-full p-2 bg-gray-700 rounded border border-gray-600"
            />
            <button type="submit" className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
              Update Title
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}