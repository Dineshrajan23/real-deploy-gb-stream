
// components/dashboard/StreamPreview.tsx
import React from 'react';
import VideoPlayer from '@/components/streamComponent/VideoPlayer';
import { CloudArrowUpIcon } from '@heroicons/react/24/outline';

interface StreamPreviewProps {
  hlsUrl: string | null;
  isLive: boolean;
  title: string;
}

const StreamPreview: React.FC<StreamPreviewProps> = ({ hlsUrl, isLive, title }) => {
  if (isLive && hlsUrl) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-semibold mb-4 text-white">Live Stream Preview</h2>
        <VideoPlayer src={hlsUrl} isLive={isLive} title={title} posterImage="/path/to/your/poster.jpg" />
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4 text-white">Live Stream Preview</h2>
      <div className="w-full aspect-video bg-gray-900 rounded-lg flex items-center justify-center p-6">
        <div className="text-center">
          <CloudArrowUpIcon className="h-16 w-16 text-gray-500 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-white mb-2">Upload and publish a video to get started</h3>
          <p className="text-gray-400 mb-4">Start streaming from OBS to go live!</p>
          <button className="px-6 py-3 bg-purple-600 text-white font-bold rounded-full hover:bg-purple-700 transition-colors">
            Upload Video
          </button>
        </div>
      </div>
    </div>
  );
};

export default StreamPreview;