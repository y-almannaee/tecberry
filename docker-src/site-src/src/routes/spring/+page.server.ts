import { error } from "@sveltejs/kit";

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
	return 1;
	const res = await fetch('/api/spring');
	const spring_data = await res.json();
	if(!spring_data.accepted) {
		throw error(403, 'Not accepting springboard right now')
	}
	return { spring_data };
  }