/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    darkMode: 'class',
    theme: {
        fontFamily: {
            'sans': ['Ubuntu', 'sans-serif'],
            'serif': ['Times New Roman', 'serif'],
            'mono': ['Fira Mono', 'mono'],
        },
        extend: {},
    },
    plugins: [],
}