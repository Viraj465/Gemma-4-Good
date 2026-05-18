/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        background: '#0F172A', // slate-900
        surface: '#1E293B',    // slate-800
        primary: '#38BDF8',    // sky-400
        secondary: '#818CF8',  // indigo-400
        text: '#F8FAFC',       // slate-50
        textMuted: '#94A3B8',  // slate-400
      },
    },
  },
  plugins: [],
}