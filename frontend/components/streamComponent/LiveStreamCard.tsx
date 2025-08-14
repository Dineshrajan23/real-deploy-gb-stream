'use client';

import { LiveStream } from '@/hooks/streamHooks/useLiveStream';
import VideoPlayer from './VideoPlayer';

interface Props {
  stream: LiveStream;
}

export default function LiveStreamCard({ stream }: Props) {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">
        {stream.title || `Stream by ${stream.user.username}`}
      </h2>
      <VideoPlayer
        src={stream.hls_url!}
        isLive={true}
        title={stream.title || `Stream by ${stream.user.username}`}
      />
    </div>
  );
}
