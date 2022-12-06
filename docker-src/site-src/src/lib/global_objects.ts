import { writable } from "svelte/store";
import { browser, dev } from '$app/environment';
import { asyncReadable } from '@square/svelte-store';

export function backend_url(path) {
	if (dev) {
		if (browser)
			return `${window.location.protocol}//${window.location.hostname}:3636${path}`;
		else
			return `http://localhost:3636${path}`;
	} else if (browser) {
		return `${window.location.origin}/api${path}`
	} else {
		return `http://controller:3636${path}`
	}
}

export const configuration = asyncReadable({}, async () => {
	let backend_conf = backend_url('/configuration');
	let conf_ok = false;
	while (!conf_ok) {
		try {
			const res = await fetch(backend_conf);
			if (res && res.ok) {
				let conf_data = await res.json()
				conf_ok = true;
				return conf_data
			}
		} catch (e) {
			conf_ok = false;
			await new Promise((r,e)=>setTimeout(r,1500))
		}
	}
});