import { backend_url, configuration } from "$lib/global_objects";

/** @type {import('./$types').LayoutServerLoad} */
export async function load({ fetch, params, url, locals }) {
	if (locals.userdata && locals.userdata.loggedIn) {
		return { loggedIn: true, name: locals.userdata.name, pfp: locals.userdata.pfp, rank: locals.userdata.rank };
	} else if (locals.userdata && locals.userdata.backend_error) {
		return { backend_error: true }
	} else {
		return { loggedIn: false }
	}
}