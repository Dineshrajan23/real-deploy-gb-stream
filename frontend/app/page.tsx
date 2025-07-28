'use client';

import { useState, useEffect } from 'react';
import VideoPlayer from '../components/VideoPlayer';


type LiveStream = {
  title: string | null;
  hls_url: string | null;
  user: {
    username: string;
  };
};

export default function Home() {
  const [liveStream, setLiveStream] = useState<LiveStream | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLiveStream = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/live-streams`);
         if (!response.ok) {
         
          setLiveStream(null);
          throw new Error('Failed to fetch live streams');
        }
        const data: LiveStream[] = await response.json();
      
        if (data.length > 0) {
          setLiveStream(data[0]);
        }else {
          setLiveStream(null);
        }
      } catch (error) {
        console.error("Failed to fetch live streams", error);
      } finally {
        setLoading(false);
      }
    };

    fetchLiveStream();
    
    const interval = setInterval(fetchLiveStream, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold">Live Stream</h1>
      </div>

      <div className="w-full max-w-4xl mt-10">
        {loading ? (
          <p>Looking for live streams...</p>
        ) : liveStream && liveStream.hls_url ? (
          <div>
            <h2 className="text-2xl mb-4">{liveStream.title || `Stream by ${liveStream.user.username}`}</h2>
            <VideoPlayer src={liveStream.hls_url} />
          </div>
        ) : (
          <div className="text-center bg-violet-800 p-10 rounded-lg">
            <h2 className="text-2xl mb-4">No one is currently live.</h2>
            <p className="text-gray-400">Check back later!</p>
          </div>
        )}
      </div>
    </main>
  );
}