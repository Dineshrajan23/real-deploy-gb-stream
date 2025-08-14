
'use client';

import { useRouter } from 'next/navigation';
import AuthForm from '@/components/Auth/AuthForm';
import { useCsrfToken } from '@/hooks/csrfHooks/useCsrfToken';
import { useForm } from '@/hooks/formshooks/useForm';

const registerFields = [
  { name: 'username', label: 'Username', type: 'text' },
  { name: 'email', label: 'Email', type: 'email' },
  { name: 'password', label: 'Password', type: 'password' },
];

type RegisterValues = {
  username: string;
  email: string;
  password: string;
};

export default function RegisterPage() {
  const router = useRouter();
  const { csrfToken, isReady } = useCsrfToken();
  
  const handleRegister = async (values: RegisterValues) => {
    if (!csrfToken) {
      throw new Error("Security token not found. Please refresh and try again.");
    }

    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/register`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
      body: JSON.stringify(values),
    });

    const data = await response.json();

    if (response.ok) {
      alert('Registration successful! Please log in.');
      router.push('/login');
    } else {
      throw new Error(data.detail || 'Registration failed.');
    }
  };
  
  const { values, handleChange, handleSubmit, isSubmitting, error } = useForm<RegisterValues>(
    { username: '', email: '', password: '' },
    handleRegister
  );

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-900">
      <AuthForm
        title="Create Account"
        fields={registerFields}
        buttonText="Sign Up"
        isSubmitting={!isReady || isSubmitting}
        error={isReady ? error : 'Connecting to server...'}
        values={values}
        handleChange={handleChange}
        handleSubmit={handleSubmit}
        linkText="Already have an account?"
        linkHref="/login"
      />
    </main>
  );
}