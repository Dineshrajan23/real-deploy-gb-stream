'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import VideoPlayer from '@/components/VideoPlayer';

type DashboardData = {
  stream_key: string;
  stream_title: string | null;
  is_live: boolean;
  hls_url: string | null;
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
    <div className="flex min-h-screen bg-gray-900 text-white">
      <Sidebar />
      <main className="flex-1 p-8">
        <h1 className="text-4xl font-bold mb-10 text-white">My Dashboard</h1>
        <div className="w-full max-w-4xl mx-auto space-y-8">
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4 text-white">Live Stream Preview</h2>
            {data.is_live && data.hls_url ? (
              <VideoPlayer
                src={data.hls_url}
                isLive={data.is_live}
                title={data.stream_title || ''}
                posterImage="path/to/your/poster-image.jpg" // Add a relevant poster image
              />
            ) : (
              <div className="w-full aspect-video bg-gray-900 rounded-lg flex items-center justify-center p-6">
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-white mb-2">Stream is currently offline</h3>
                  <p className="text-gray-400 mb-4">Start streaming from OBS to go live!</p>
                  <button className="px-6 py-3 bg-purple-600 text-white font-bold rounded-full hover:bg-purple-700 transition-colors">
                    Go Live
                  </button>
                </div>
              </div>
            )}
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-semibold mb-4 text-white">Streaming Setup</h2>
              <p className="mb-2 text-gray-300"><strong>RTMP Server:</strong> <code>{process.env.NEXT_PUBLIC_RTMP_URL}/live</code></p>
              <div className="mb-4">
                <p className="mb-2 text-gray-300"><strong>Stream Key:</strong></p>
                <div className="flex items-center space-x-4 bg-gray-900 p-3 rounded-lg border border-gray-700">
                  <input
                    type={showKey ? 'text' : 'password'}
                    readOnly
                    value={data.stream_key}
                    className="bg-transparent text-white font-mono w-full focus:outline-none"
                  />
                  <button onClick={() => setShowKey(!showKey)} className="text-sm text-purple-400 hover:text-purple-300 transition-colors">
                    {showKey ? 'Hide' : 'Show'}
                  </button>
                </div>
              </div>
              <button onClick={handleResetKey} className="text-sm text-red-500 hover:text-red-400 transition-colors">
                Reset Key
              </button>
            </div>

            <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-semibold mb-4 text-white">Stream Details</h2>
              <form onSubmit={handleUpdateTitle}>
                <label htmlFor="title" className="block text-sm font-medium text-gray-300 mb-2">Stream Title</label>
                <input
                  id="title"
                  type="text"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full p-3 bg-gray-700 rounded-lg border border-gray-600 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
                <button
                  type="submit"
                  className="mt-4 w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-4 rounded-lg transition-colors"
                >
                  Update Title
                </button>
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}