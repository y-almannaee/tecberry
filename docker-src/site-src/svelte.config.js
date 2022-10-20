import adapter from '@sveltejs/adapter-auto';
//import adapter from '@sveltejs/adapter-static';
import preprocess from "svelte-preprocess";
import { trusted } from 'svelte/internal';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
        adapter: adapter({
            pages: 'build',
            assets: 'build',
            fallback: null,
            precompress: false,
        }),
    },
    prerender: {
        default: true,
    },
    preprocess: [
        preprocess({
            postcss: true,
        }),
    ],

};

export default config;