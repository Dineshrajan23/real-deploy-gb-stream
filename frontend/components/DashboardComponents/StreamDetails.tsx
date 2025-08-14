// components/dashboard/StreamDetails.tsx
import React, { useState, useEffect } from 'react';

interface StreamDetailsProps {
  streamTitle: string;
  onUpdateTitle: () => void;
}

const StreamDetails: React.FC<StreamDetailsProps> = ({ streamTitle, onUpdateTitle }) => {
  const [newTitle, setNewTitle] = useState(streamTitle);

  useEffect(() => {
    setNewTitle(streamTitle);
  }, [streamTitle]);

  const handleUpdateTitle = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/dashboard`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTitle }),
    });
    alert('Title updated!');
    onUpdateTitle();
  };

  return (
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
  );
};

export default StreamDetails;