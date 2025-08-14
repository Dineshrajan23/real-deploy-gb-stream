'use client';

import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/sideBars/Sidebar";
import Breadcrumb from "@/components/sideBars/Breadcrumb";
import { useState } from 'react';
import RightSideBar from "@/components/sideBars/RightSideBar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});


 const metadata: Metadata = {
  title: "Stream ",
  description: "GameBoss Stream - Live Streaming Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <div className="flex  min-h-screen bg-black-900 text-white">
          <Sidebar isSidebarOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
          <div className="flex-1 overflow-x-hidden p-8 transition-all duration-300">
            <div className="flex items-center mb-6">
              <Breadcrumb onToggle={toggleSidebar} />

            </div>
            {children}
      
          </div>
                <RightSideBar/>
        </div>
     
      </body>
    </html>
  );
}