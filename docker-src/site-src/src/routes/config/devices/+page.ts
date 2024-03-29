// from https://kit.svelte.dev/docs/routing#page
import { error } from '@sveltejs/kit';
import { backend_url } from '$lib/global_objects';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, params, url }) {
	let backend = backend_url('/devices')
	const res = await fetch(backend);
	if (res !== undefined && res.ok) {
		const json = await res.json();
		return {
			devices: json.devices
		}
	} else {
		throw error(502, 'backend error');
	}
}