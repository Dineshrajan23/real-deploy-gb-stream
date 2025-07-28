'use client';

import React, { useEffect, useRef } from 'react';
import Hls from 'hls.js';


interface VideoPlayerProps {
  src: string;
}


const VideoPlayer: React.FC<VideoPlayerProps> = ({ src }) => {

  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(src);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.play().catch(error => {
          console.error("Video play failed:", error);
        });
      });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = src;
      video.addEventListener('loadedmetadata', () => {
        video.play().catch(error => {
          console.error("Video play failed:", error);
        });
      });
    }
  }, [src]); 

  return <video ref={videoRef} controls style={{ width: '100%' }} />;
};

export default VideoPlayer;