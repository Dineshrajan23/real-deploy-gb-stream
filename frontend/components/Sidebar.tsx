'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import Image from 'next/image';

type StreamStatus = {
  is_live: boolean;
};

export default function Sidebar() {
  const pathname = usePathname();
  const [isLive, setIsLive] = useState(false);

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
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/recordings', label: 'Recordings' },
    { href: '/', label: 'Streamers & Videos', isLive: isLive },
    { href: '/community', label: 'Communities & Chat' },
    { href: '/settings', label: 'Settings' },
  ];

  return (
    <aside className="w-64 flex-none min-h-screen bg-gray-900 text-white p-6 flex flex-col border-r border-gray-800">
      <div className="flex items-center mb-6">
        <Image
          src="/logo/gameboss_logo.svg"
          alt="Logo"
          width={100}
          height={60}
          className="mr-2"
        />
      </div>
      <nav>
        <ul>
          {navItems.map((item) => (
            <li key={item.href} className="mb-4">
              <Link href={item.href}>
                <div
                  className={`flex items-center p-3 rounded-lg transition-colors ${
                    pathname === item.href 
                      ? 'text-purple-500'
                      : 'hover:text-purple-400' 
                  }`}
                >
                  {item.label}
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
  );
}