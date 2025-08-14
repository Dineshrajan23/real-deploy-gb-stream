'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import Image from 'next/image';


import { FaHome, FaTachometerAlt, FaVideo, FaUsers, FaCog } from 'react-icons/fa';

type StreamStatus = {
  is_live: boolean;
};

interface SidebarProps {
  isSidebarOpen: boolean;
  onClose: () => void;
}

export default function Sidebar({ isSidebarOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const [isLive, setIsLive] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    const checkStreamStatus = async () => {
      try {
        const response = await fetch('/api/dashboard');
        if (response.ok) {
          const data: StreamStatus = await response.json();
          setIsLive(data.is_live);
        } else {
          setIsLive(false);
        }
      } catch (error) {
        setIsLive(false);
      }
    };

    checkStreamStatus();
    const interval = setInterval(checkStreamStatus, 15000);

    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { href: '/dashboard', label: 'Dashboard', icon: FaTachometerAlt },
    { href: '/recordings', label: 'Recordings', icon: FaVideo },
    { href: '/', label: 'Streamers & Videos', isLive: isLive, icon: FaHome },
    { href: '/community', label: 'Communities & Chat', icon: FaUsers },
    { href: '/settings', label: 'Settings', icon: FaCog },
  ];

  const sidebarWidth = isHovered ? 'w-64' : 'w-20';

  return (
    <>
      {/* Mobile Overlay */}
      <div
        className={`fixed inset-0 z-40 bg-black bg-opacity-50 transition-opacity duration-300 ${isSidebarOpen ? 'opacity-100 lg:hidden' : 'opacity-0 pointer-events-none'}`}
        onClick={onClose}
      ></div>

      <aside
        className={`fixed inset-y-0 left-0 z-50 flex flex-col bg-zinc-900 text-white p-6 border-r border-gray-800 transition-all duration-300
        ${isSidebarOpen ? 'w-64' : 'w-20'} lg:static lg:flex-none
        ${!isSidebarOpen && !isHovered ? 'lg:w-20' : 'lg:w-64'}
        ${isSidebarOpen ? 'translate-x-2' : '-translate-x-full'} lg:translate-x-0`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <div className={`flex items-center mb-6 transition-opacity duration-300 ${isHovered || isSidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
          <Image
            src="/logo/gameboss_logo.svg"
            alt="Logo"
            width={100}
            height={40}
            className="mr-2"
          />
          <span className={`font-bold text-2xl transition-all duration-300 ${isHovered || isSidebarOpen ? 'ml-0' : 'ml-2'}`}></span>
        </div>

        <nav className="mt-6">
          <ul>
            {navItems.map((item) => (
              <li key={item.href} className="mb-4">
                <Link href={item.href}>
                  <div
                    onClick={onClose}
                    className={`flex items-center p-3 rounded-lg transition-colors duration-200
      ${pathname === item.href
                        ? 'text-purple-500'
                        : 'text-gray-400 hover:text-purple-600'}`}
                  >
                    <item.icon
                      className={`text-xl transition-all duration-300 
        ${isHovered || isSidebarOpen ? 'mr-4' : '-mr-2'}`}
                    />

                    <span
                      className={`whitespace-nowrap transition-all duration-300 overflow-hidden text-1xl 
        ${pathname === item.href
                          ? 'bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent'
                          : 'text-white'} 
        ${isHovered || isSidebarOpen ? 'opacity-100 w-auto' : 'opacity-0 w-0'}`}
                    >
                      {item.label}
                    </span>

                    {item.isLive && item.href === '/' && (
                      <span className="ml-auto w-3 h-3 bg-violet-600 rounded-full animate-pulse"></span>
                    )}
                  </div>
                </Link>

              </li>
            ))}
          </ul>
        </nav>
      </aside>
    </>
  );
}