'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';


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
    { href: '/', label: 'Live Stream', isLive: isLive },
  ];

  return (
    <aside className="w-64 bg-gray-900 text-white p-6 flex flex-col">
      <h1 className="text-2xl font-bold mb-10">My Platform</h1>
      <nav>
        <ul>
          {navItems.map((item) => (
            <li key={item.href} className="mb-4">
              <Link href={item.href}>
                <div
                  className={`flex items-center p-3 rounded-lg hover:bg-gray-700 transition-colors ${
                    pathname === item.href ? 'bg-blue-600' : ''
                  }`}
                >
                  {item.label}
                  {item.isLive && (
                    <span className="ml-auto w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
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