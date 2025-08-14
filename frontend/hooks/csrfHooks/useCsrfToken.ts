// hooks/useCsrfToken.ts
'use client';

import { useState, useEffect } from 'react';
import { getCookie } from '../../utils/getCookie';

export const useCsrfToken = () => {
  const [isReady, setIsReady] = useState(false);
  const [csrfToken, setCsrfToken] = useState<string | null>(null);

  useEffect(() => {
    const ensureCsrfCookie = async () => {
      try {
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/csrf-cookie`, {
          credentials: 'include',
        });
        const token = getCookie('csrftoken');
        setCsrfToken(token);
      } catch (err) {
        console.error("Failed to fetch CSRF cookie", err);
      } finally {
        setIsReady(true);
      }
    };
    ensureCsrfCookie();
  }, []);

  return { isReady, csrfToken };
};