/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1a73e8',
        secondary: '#5f6368',
        success: '#34a853',
        warning: '#fbbc05',
        error: '#ea4335',
      },
    },
  },
  plugins: [],
}
