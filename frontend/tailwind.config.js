/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#080715",
        surface: "rgba(15, 14, 35, 0.75)",
        sidebar: "rgba(12, 10, 28, 0.85)",
        accent: {
          purple: "#a855f7",
          cyan: "#06b6d4",
          magenta: "#ec4899",
          blue: "#3b82f6",
        }
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 3s ease-in-out infinite',
        'wave': 'wave 8s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: '0.6', filter: 'drop-shadow(0 0 15px rgba(168, 85, 247, 0.4))' },
          '50%': { opacity: '1', filter: 'drop-shadow(0 0 25px rgba(236, 72, 153, 0.7))' },
        },
      }
    },
  },
  plugins: [],
}
