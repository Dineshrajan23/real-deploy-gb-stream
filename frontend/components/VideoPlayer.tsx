'use client';

import React, { useEffect, useRef, useState } from 'react';
import Hls from 'hls.js';

interface VideoPlayerProps {
  src: string;
  isLive: boolean;
  title: string;
  posterImage?: string; 
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ src, isLive, title, posterImage }) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showOverlay, setShowOverlay] = useState(true);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video || !src) return;

    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(src);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.play().catch(error => {
          console.error("Video play failed:", error);
        });
        setIsPlaying(true);
        setShowOverlay(false);
      });
      return () => {
        hls.destroy();
      };
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = src;
      video.addEventListener('loadedmetadata', () => {
        video.play().catch(error => {
          console.error("Video play failed:", error);
        });
        setIsPlaying(true);
        setShowOverlay(false);
      });
    }
  }, [src]);

  const handlePlayPause = () => {
    const video = videoRef.current;
    if (video) {
      if (isPlaying) {
        video.pause();
      } else {
        video.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleOverlayClick = () => {
    const video = videoRef.current;
    if (video) {
      video.play();
      setShowOverlay(false);
      setIsPlaying(true);
    }
  };

  return (
    <div
      className="relative w-full aspect-video bg-black rounded-lg overflow-hidden"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <video
        ref={videoRef}
        poster={posterImage}
        className="w-full h-full object-cover"
        onClick={handlePlayPause}
      />

      {isLive && (
        <div className="absolute top-4 left-4 z-10">
          <div className="flex items-center px-2 py-1 bg-red-600 rounded-full text-white text-xs font-semibold">
            <span className="w-2 h-2 mr-2 bg-white rounded-full animate-pulse"></span>
            LIVE
          </div>
        </div>
      )}

      <div className={`absolute inset-x-0 bottom-0 p-4 transition-opacity duration-300 ${isHovered || !isPlaying ? 'opacity-100' : 'opacity-0'}`}>
        <div className="relative h-1 bg-gray-600 rounded-full cursor-pointer">
          <div className="absolute top-0 left-0 h-1 bg-red-600 rounded-full" style={{ width: '100%' }}></div>
        </div>
        <button
          onClick={handlePlayPause}
          className="mt-2 text-white bg-transparent border-none focus:outline-none"
        >
          {isPlaying ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm4 0a1 1 0 012 0v4a1 1 0 11-2 0V8z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
            </svg>
          )}
        </button>
      </div>

      {showOverlay && (
        <div className="absolute inset-0 flex items-center justify-center p-6 bg-black bg-opacity-70">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-white mb-2">{title || 'Stream is offline'}</h2>
            <p className="text-gray-300 mb-4">Start streaming to go live!</p>
            <button
              onClick={handleOverlayClick}
              className="px-6 py-3 bg-red-600 text-white font-bold rounded-full hover:bg-red-700 transition-colors"
            >
              Watch
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoPlayer;