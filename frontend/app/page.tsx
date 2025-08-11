'use client';

import LiveStreamFeed from '@/components/LiveStreamFeed';

export default function Home() {
  return (
    <div className="flex flex-col items-center p-8 w-full">
      <div className="w-full max-w-4xl">
        <h1 className="text-4xl font-bold mb-8">Live Streams</h1>
      </div>
      <div className="w-full max-w-4xl">
        <LiveStreamFeed />
      </div>
    </div>
  );
}