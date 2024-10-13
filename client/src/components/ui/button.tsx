import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline';
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'default',
  className = '',
  ...props
}) => {
  const baseStyles = 'px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-offset-2';
  const variantStyles = variant === 'outline'
    ? 'border border-gray-300 text-gray-700 hover:bg-gray-50'
    : 'bg-blue-500 text-white hover:bg-blue-600';

  return (
    <button
      className={`${baseStyles} ${variantStyles} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};