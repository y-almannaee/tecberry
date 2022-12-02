// from https://kit.svelte.dev/docs/routing#page
import { error, json } from '@sveltejs/kit';
import { devices, backend_url } from '$lib/global_objects';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params, url }) {
	let backend_devices = backend_url('/devices');
	const res_devices = await fetch(backend_devices);
	let backend_scheduler = backend_url('/scheduler');
	const res_scheduler = await fetch(backend_scheduler);
	if (res_devices !== undefined && res_devices.ok && res_scheduler !== undefined && res_scheduler.ok) {
		const json_devices = await res_devices.json();
		const json_scheduler = await res_scheduler.json()
		let scheduler_data = {
			duration: json_scheduler.duration || 300,
			amplitude: json_scheduler.amplitude || 55,
			offset: json_scheduler.offset || 25,
			period: json_scheduler.period || 150,
			phase_shift: json_scheduler.phase_shift || 0,
			on_start_code: json_scheduler.on_start_code || '',
			on_end_code: json_scheduler.on_end_code || '',
			device_exec_order: json_scheduler.device_exec_order || undefined
		}
		return {
			devices: json_devices.devices,
			scheduler: json_scheduler
		}
	} else {
		throw error(502, 'backend error');
	}
}