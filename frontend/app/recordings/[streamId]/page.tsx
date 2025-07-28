'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
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

export default function RecordingPlaybackPage() {
  const params = useParams();
  const recordingID = params.streamId;

  const [recording, setRecording] = useState<Recording | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (recordingID) {
      const fetchRecording = async () => {
        try {
            const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/recordings/${recordingID}`;
            const response = await fetch(apiUrl);
          if (!response.ok) {
            throw new Error('Recording not found');
          }
          const data = await response.json();
          setRecording(data);
        } catch (err) {
          setError((err as Error).message);
        }
      };
      fetchRecording();
    }
  }, [recordingID]);

  if (error) {
    return <main className="p-24"><p>Error: {error}</p></main>;
  }

  if (!recording) {
    return <main className="p-24"><p>Loading...</p></main>;
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <div className="w-full max-w-4xl">
        <h1 className="text-4xl font-bold mb-4">{recording.stream.title || `Stream by ${recording.stream.user.username}`}</h1>
        <p className="text-gray-400 mb-8">Recorded on {new Date(recording.created_at).toLocaleString()}</p>

        <video
          src={recording.file_path}
          controls
          autoPlay
          style={{ width: '100%', borderRadius: '8px' }}
        />

                <div className="mt-8">
            <Link href="/recordings" className="text-violet-800 hover:text-violet-600">
                ← Back to all recordings
            </Link>
        </div>
      </div>
    </main>
  );
}