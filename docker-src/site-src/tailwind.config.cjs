/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        require('path').join(require.resolve('@brainandbones/skeleton'), '../**/*.{.html,js,svelte,ts}'),
        './src/**/*.{html,js,svelte,ts}'
    ],
    safelist: [{
        pattern: /(bg|text|hover:bg)-./,
    }],
    darkMode: 'class',
    theme: {
        fontFamily: {
            'sans': ['Ubuntu', 'sans-serif'],
            'serif': ['Times New Roman', 'serif'],
            'mono': ['Fira Mono', 'mono'],
        },
        extend: {},
    },
    plugins: [
        require('@brainandbones/skeleton/tailwind/theme.cjs'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        function({ addBase, theme }) {
            function extractColorVars(colorObj, colorGroup = '') {
                return Object.keys(colorObj).reduce((vars, colorKey) => {
                    const value = colorObj[colorKey];

                    const newVars =
                        typeof value === 'string' ? {
                            [`--color${colorGroup}-${colorKey}`]: value
                        } :
                        extractColorVars(value, `-${colorKey}`);

                    return {...vars, ...newVars };
                }, {});
            }

            addBase({
                ':root': extractColorVars(theme('colors')),
            });
        },
    ],
}