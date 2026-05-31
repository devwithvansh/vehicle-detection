export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        bunker: '#080b08',
        field: '#10160f',
        olive: '#64743a',
        moss: '#8b9b4f',
        amber: '#f2c94c',
        danger: '#d35d4f'
      },
      boxShadow: {
        tactical: '0 20px 80px rgba(0,0,0,0.35)'
      }
    }
  },
  plugins: []
}
