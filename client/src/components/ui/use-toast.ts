interface ToastOptions {
    title: string;
    description: string;
    variant?: 'default' | 'destructive';
  }
  
  export const toast = ({ title, description, variant = 'default' }: ToastOptions) => {
    // 这里是一个简单的实现，实际应用中您可能想使用一个更复杂的toast库
    const toastElement = document.createElement('div');
    toastElement.className = `fixed bottom-4 right-4 bg-white shadow-lg rounded-lg p-4 ${
      variant === 'destructive' ? 'border-l-4 border-red-500' : 'border-l-4 border-blue-500'
    }`;
    toastElement.innerHTML = `
      <h3 class="font-bold">${title}</h3>
      <p>${description}</p>
    `;
    document.body.appendChild(toastElement);
  
    setTimeout(() => {
      document.body.removeChild(toastElement);
    }, 3000);
  };