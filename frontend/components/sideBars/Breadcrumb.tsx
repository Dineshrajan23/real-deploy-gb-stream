'use client';

import React from 'react';

interface BreadcrumbProps {
  onToggle: () => void;
}

const Breadcrumb: React.FC<BreadcrumbProps> = ({ onToggle }) => {
  return (
    <button
      onClick={onToggle}
      className="p-2 text-white hover:text-purple-400 focus:outline-none lg:hidden"
    >
      <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>
  );
};

export default Breadcrumb;