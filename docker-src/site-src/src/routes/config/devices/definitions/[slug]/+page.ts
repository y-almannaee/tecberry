// from https://kit.svelte.dev/docs/routing#page
import { error, json } from '@sveltejs/kit';
import { backend_url } from '$lib/global_objects';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params, url }) {
	let backend = backend_url('/definitions');
	const res = await fetch(backend);
	if (res !== undefined && res.ok) {
		const json = await res.json();
		return json.definitions.find((test)=>test.id==params.slug);
	} else {
		throw error(502, 'backend error');
	}
}