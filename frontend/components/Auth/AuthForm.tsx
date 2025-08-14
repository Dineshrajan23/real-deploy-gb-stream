// components/auth/AuthForm.tsx
import React, { FormEvent, ChangeEvent } from 'react';
import Link from 'next/link';

interface AuthFormProps {
  title: string;
  fields: { name: string; label: string; type: string }[];
  buttonText: string;
  isSubmitting: boolean;
  error: string | null;
  values: { [key: string]: string }; 
  handleChange: (e: ChangeEvent<HTMLInputElement>) => void;
  handleSubmit: (e: FormEvent) => void;
  linkText?: string;
  linkHref?: string;
}

const AuthForm: React.FC<AuthFormProps> = ({
  title,
  fields,
  buttonText,
  isSubmitting,
  error,
  values,
  handleChange,
  handleSubmit,
  linkText,
  linkHref,
}) => {
  return (
    <div className="w-full max-w-md">
      <form onSubmit={handleSubmit} className="bg-gray-800 shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h1 className="text-2xl font-bold mb-6 text-center text-white">{title}</h1>
        {error && <p className="bg-red-500 text-white text-center p-2 rounded mb-4">{error}</p>}
        
        {fields.map(field => (
          <div className="mb-4" key={field.name}>
            <label className="block text-gray-300 text-sm font-bold mb-2" htmlFor={field.name}>
              {field.label}
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 bg-gray-700 text-white"
              id={field.name}
              name={field.name}
              type={field.type}
              value={values[field.name]}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        <div className="flex flex-col items-center justify-between">
          <button 
            className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded w-full disabled:bg-gray-500" 
            type="submit"
            disabled={isSubmitting} 
          >
            {isSubmitting ? '...' : buttonText}
          </button>
          {linkText && linkHref && (
            <Link href={linkHref} className="inline-block align-baseline font-bold text-sm text-purple-400 hover:text-purple-300 mt-4">
              {linkText}
            </Link>
          )}
        </div>
      </form>
    </div>
  );
};

export default AuthForm;