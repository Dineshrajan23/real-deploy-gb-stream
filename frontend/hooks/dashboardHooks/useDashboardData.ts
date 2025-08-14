'use client';

import { useState, useEffect } from 'react';

type DashboardData = {
  stream_key: string;
  stream_title: string | null;
  is_live: boolean;
  hls_url: string | null;
  username: string;
};

export const useDashboardData = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    setError(null);
    try {
 
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/dashboard`, {

        credentials: 'include', 
      });

      if (response.status === 401) {
        throw new Error('401 Unauthorized');
      }
      if (!response.ok) {
        throw new Error(`Failed to fetch dashboard data: ${response.statusText}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return { data, isLoading, error, refetchData: fetchDashboardData };
};