module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef6ff',
          100: '#d9ebff',
          200: '#bfe0ff',
          300: '#8bc7ff',
          400: '#59a9ff',
          500: '#2d8cff',
          600: '#176de6',
          700: '#1456c3',
          800: '#1848a1',
          900: '#1a3f7e'
        }
      },
      boxShadow: {
        glow: '0 0 40px rgba(45, 140, 255, 0.35)'
      }
    }
  },
  plugins: []
};
