// from https://kit.svelte.dev/docs/routing#page
import { error } from '@sveltejs/kit';
import { instances } from '$lib/global_objects';
import { browser } from '$app/environment';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, params, url }) {
	let backend_url = browser ? `${url.origin}/api/devices` : 'http://127.0.0.1:80/devices';
	console.log(backend_url)
	const res = await fetch(backend_url);
	console.log(res)
	if (res !== undefined && res.ok()) {
		const json = await res.json();
		instances.set(json);
	} else {
		throw error(502, 'backend error');
	}
	return {
		devices: instances
	}
}