// from https://kit.svelte.dev/docs/routing#page
import { error } from '@sveltejs/kit';
import { backend_url } from '$lib/global_objects';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params, url }) {
	let backend_defs = backend_url('/definitions');
	const res_defs = await fetch(backend_defs);
	let json_defs_ = [];
	if (res_defs !== undefined && res_defs.ok) {
		const json_defs = await res_defs.json();
		json_defs_=json_defs;
	}
	let backend = backend_url('/devices')
	const res = await fetch(backend);
	if (res !== undefined && res.ok) {
		const json = await res.json();
		return {self: json.devices.find((test) => test.id == params.slug), devices: json.devices, definitions: json_defs_.definitions};
	} else {
		throw error(502, 'backend error');
	}
}