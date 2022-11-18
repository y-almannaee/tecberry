// import adapter from '@sveltejs/adapter-auto';
// import adapter from '@sveltejs/adapter-static';
import adapter from '@sveltejs/adapter-node';
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
            envPrefix: 'SVELTEKIT_'
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