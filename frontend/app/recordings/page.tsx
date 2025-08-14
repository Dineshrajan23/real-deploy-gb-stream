'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

type Recording = {
  id: number;
  file_path: string;
  created_at: string;
  stream: {
    title: string | null;
    user: {
      username: string;
    };
  };
};

export default function RecordingsPage() {
  const [recordings, setRecordings] = useState<Recording[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecordings = async () => {
      try {
        const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/recordings`;
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error('Failed to fetch recordings');
        }
        const data = await response.json();
        setRecordings(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecordings();
  }, []);

  if (loading) {
    return <main className="p-24"><p>Loading recordings...</p></main>;
  }

  return (
    <main className="flex  min-h-screen flex-col  items-center  p-24">
      <h1 className="text-4xl  font-italic md:text-3xl sm:text-2xl mb-10">Past Streams</h1>
      <div className="w-full max-w-4xl">
        {recordings.length > 0 ? (
          <ul className="space-y-4">
            {recordings.map((rec) => (
              <li key={rec.id} className="bg-gray-800 p-4 rounded-lg hover:bg-gray-700 transition-colors ">
                <Link href={`/recordings/${rec.id}`}>
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="text-xl font-semibold">{rec.stream.title || `Stream by ${rec.stream.user.username}`}</p>
                      <p className="text-sm text-gray-400">
                        {new Date(rec.created_at).toLocaleString()}
                      </p>
                    </div>
                    <span className="text-blue-400">Watch Now →</span>
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        ) : (
           <div className="text-center bg-gray-800 p-10 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-4 ">No recordings found.</h2>
            <p className="text-gray-400 ">This page will update once you finish a stream.</p>
          </div>
        )}
      </div>
    </main>
  );
}