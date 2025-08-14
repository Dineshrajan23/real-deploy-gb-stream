
'use client';

import { useRouter } from 'next/navigation';
import AuthForm from '@/components/Auth/AuthForm';
import { useCsrfToken } from '@/hooks/csrfHooks/useCsrfToken';
import { useForm } from '@/hooks/formshooks/useForm';

const loginFields = [
  { name: 'username', label: 'Username', type: 'text' },
  { name: 'password', label: 'Password', type: 'password' },
];

type LoginValues = {
  username: string;
  password: string;
};

export default function LoginPage() {
  const router = useRouter();
  const { csrfToken, isReady } = useCsrfToken();
  
  const handleLogin = async (values: LoginValues) => {
    if (!csrfToken) {
      throw new Error("Could not verify security token. Please refresh the page.");
    }
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/login`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify(values),
    });

    if (response.ok) {
      window.location.href = '/dashboard';
    } else {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Invalid username or password.');
    }
  };

  const { values, handleChange, handleSubmit, isSubmitting, error } = useForm<LoginValues>(
    { username: '', password: '' },
    handleLogin
  );
  
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-900">
      <AuthForm
        title="Login"
        fields={loginFields}
        buttonText="Sign In"
        isSubmitting={!isReady || isSubmitting}
        error={isReady ? error : 'Connecting to server...'}
        values={values}
        handleChange={handleChange}
        handleSubmit={handleSubmit}
        linkText="Don't have an account?"
        linkHref="/register"
      />
    </main>
  );
}