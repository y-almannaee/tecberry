
import { goto } from '$app/navigation';
import { browser } from '$app/environment';

/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, parent, params, url }) {
	const { backend_error } = await parent()
	if (backend_error && browser) console.log("NOOP")
	else if (browser)
		goto('/stats/insight');
}