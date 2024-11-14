/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      spacing: {
        '1/8': '12.5%',
        '1/10': '10%',
        'delay-25': 'transition-delay-25',
        '46': '46px',
      },
      transitionDelay: {
        '20': '20ms',
      }
    }
  },
  plugins: [
    require('flowbite/plugin')
  ]
}
