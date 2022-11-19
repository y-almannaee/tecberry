// from https://kit.svelte.dev/docs/routing#page
import { error } from '@sveltejs/kit';
 
/** @type {import('./$types').PageLoad} */
export function load({ params }) {
  //if (params.slug === 'hello-world') {
    return {
		name: 'Example definition',
		id: parseInt(params.slug),
		desc: 'Example description of the definition'
	  }
}