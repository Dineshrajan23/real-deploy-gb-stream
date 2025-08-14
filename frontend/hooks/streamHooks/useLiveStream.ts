'use client';

import { useState, useEffect, useRef } from 'react';

export type LiveStream = {
  title: string | null;
  hls_url: string | null;
  user: { username: string };
};

interface Options {
  interval?: number; 
}

export function useLiveStream({ interval = 15000 }: Options = {}) {
  const [liveStream, setLiveStream] = useState<LiveStream | null>(null);
  const [loading, setLoading] = useState(true);
  const prevDataRef = useRef<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    const fetchLiveStream = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/live-streams`,
          { signal: controller.signal }
        );

        if (!res.ok) {
          if (isMounted) setLiveStream(null);
          return;
        }

        const data: LiveStream[] = await res.json();
        const stream = data.length > 0 ? data[0] : null;
        const serialized = JSON.stringify(stream);

        if (serialized !== prevDataRef.current) {
          prevDataRef.current = serialized;
          if (isMounted) setLiveStream(stream);
        }
      } catch (err: any) {
        if (err.name !== 'AbortError') {
          console.error('Live stream fetch error:', err);
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchLiveStream();
    const id = setInterval(fetchLiveStream, interval);

    return () => {
      isMounted = false;
      controller.abort();
      clearInterval(id);
    };
  }, [interval]);

  return { liveStream, loading };
}
