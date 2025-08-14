// components/dashboard/StreamSetup.tsx
import React, { useState } from 'react';

interface StreamSetupProps {
  streamKey: string;
  onResetKey: () => void;
}

const StreamSetup: React.FC<StreamSetupProps> = ({ streamKey, onResetKey }) => {
  const [showKey, setShowKey] = useState(false);

  const handleResetKey = async () => {
    if (confirm('Are you sure you want to reset your stream key?')) {
      await fetch('/api/dashboard/reset-key', { method: 'POST' });
      alert('Stream key has been reset.');
      onResetKey();
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4 text-white">Streaming Setup</h2>
      <p className="mb-2 text-gray-300"><strong>RTMP Server:</strong> <code>{process.env.NEXT_PUBLIC_RTMP_URL}/live</code></p>
      <div className="mb-4">
        <p className="mb-2 text-gray-300"><strong>Stream Key:</strong></p>
        <div className="flex items-center space-x-4 bg-gray-900 p-3 rounded-lg border border-gray-700">
          <input
            type={showKey ? 'text' : 'password'}
            readOnly
            value={streamKey}
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
  );
};

export default StreamSetup;