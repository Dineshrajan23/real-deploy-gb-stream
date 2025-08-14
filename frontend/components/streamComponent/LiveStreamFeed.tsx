'use client';

import { useLiveStream } from '@/hooks/streamHooks/useLiveStream';
import LiveStreamCard from './LiveStreamCard';

export default function LiveStreamFeed() {
  const { liveStream, loading } = useLiveStream({ interval: 15000 });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-lg text-gray-400">Looking for live streams...</p>
      </div>
    );
  }

  if (liveStream?.hls_url) {
    return <LiveStreamCard stream={liveStream} />;
  }

  return (
    <div className="text-center bg-gray-800 p-10 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">No one is currently live.</h2>
      <p className="text-gray-400">Check back soon for new streams!</p>
    </div>
  );
}
