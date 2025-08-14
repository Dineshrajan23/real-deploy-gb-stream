'use client';

import { useRouter } from 'next/navigation';
import DashboardHeader from '@/components/DashboardComponents/DashboardHeaders';
import StreamDetails from '@/components/DashboardComponents/StreamDetails';
import StreamSetup from '@/components/DashboardComponents/StreamSetup';
import StreamPreview from '@/components/DashboardComponents/StreamPreview';
import Link from 'next/link';
import { useDashboardData } from '@/hooks/dashboardHooks/useDashboardData';

export default function DashboardPage() {
  const router = useRouter();
  const { data, isLoading, error, refetchData } = useDashboardData();

  if (isLoading) {
    return (
      <main className="p-24 flex items-center justify-center min-h-screen bg-gray-900 text-white">
        <p>Loading dashboard...</p>
      </main>
    );
  }

  if (error && error.includes('401')) {
    router.push('/login');
    return null;
  }

  if (error) {
    return (
      <main className="p-24 flex items-center justify-center min-h-screen bg-gray-900 text-white">
        <div className="text-center">
          <p className="text-xl mb-4">{error}</p>
          <button
            onClick={refetchData}
            className="px-6 py-3 bg-purple-600 text-white font-bold rounded-full hover:bg-purple-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </main>
    );
  }

  // Handle the case where no data is returned after loading
  if (!data) {
    return (
      <main className="p-24 flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">You are not logged in or your account is not set up.</h2>
          <p className="mb-4 text-gray-400">
            Please log in or contact support.
          </p>
          <div className="flex space-x-4 justify-center">
            <Link href="/login" className="px-6 py-3 bg-purple-600 text-white font-bold rounded-full hover:bg-purple-700 transition-colors">
              Go to Login
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      <DashboardHeader username={data.username} />
      <main className="flex-1 p-8">
        <div className="w-full max-w-7xl mx-auto space-y-8">
          <StreamPreview hlsUrl={data.hls_url} isLive={data.is_live} title={data.stream_title || ''} />
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <StreamSetup streamKey={data.stream_key} onResetKey={refetchData} />
            <StreamDetails streamTitle={data.stream_title || ''} onUpdateTitle={refetchData} />
          </div>
        </div>
      </main>
    </div>
  );
}
