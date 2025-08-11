'use client';

import { useState, useEffect } from 'react';
import VideoPlayer from './VideoPlayer';

type LiveStream = {
  title: string | null;
  hls_url: string | null;
  user: {
    username: string;
  };
};

const LiveStreamFeed = () => {
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
        } else {
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-lg text-gray-400">Looking for live streams...</p>
      </div>
    );
  }

  if (liveStream && liveStream.hls_url) {
    return (
      <div className="space-y-4">
        <h2 className="text-2xl font-bold">{liveStream.title || `Stream by ${liveStream.user.username}`}</h2>
        <VideoPlayer 
          src={liveStream.hls_url} 
          isLive={true} 
          title={liveStream.title || `Stream by ${liveStream.user.username}`}
        />
      </div>
    );
  }

  return (
    <div className="text-center bg-gray-800 p-10 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">No one is currently live.</h2>
      <p className="text-gray-400">Check back soon for new streams!</p>
    </div>
  );
};

export default LiveStreamFeed;