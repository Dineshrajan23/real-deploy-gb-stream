import React from 'react';
import Link from 'next/link';

interface DashboardHeaderProps {
  username: string;
}

const DashboardHeader: React.FC<DashboardHeaderProps> = ({ username }) => {
  return (
    <header className="bg-gray-800 p-4">
      <div className="flex items-center justify-between w-full max-w-7xl mx-auto">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold">
            {username.charAt(0).toUpperCase()}
          </div>
          <h2 className="text-xl font-bold">{username}</h2>
        </div>
        <nav className="hidden md:flex space-x-6">
          <Link href="/dashboard" className="text-gray-300 hover:text-white">Dashboard</Link>
          <Link href="/stats" className="text-gray-300 hover:text-white">Stats</Link>
          <Link href="/settings" className="text-gray-300 hover:text-white">Settings</Link>
        </nav>
      </div>
    </header>
  );
};

export default DashboardHeader;