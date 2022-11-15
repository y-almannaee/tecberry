<script>
	import {slide} from 'svelte/transition';
	let anim = true;

	let data = {};
	data.devices = [
		{id: 0, name: "Example 1", desc: "An example device"},
		{id: 1, name: "Example 2", desc: "An example device"},
		{id: 2, name: "Example 1", desc: "An example device"},
		{id: 3, name: "Example 2", desc: "An example device"},
		{id: 4, name: "Example 1", desc: "An example device"},
		{id: 5, name: "Example 2", desc: "An example device"},
		{id: 6, name: "Example 1", desc: "An example device"},
		{id: 7, name: "Example 2", desc: "An example device"},
	];
</script>

{#each data.devices as device (device.id)}
<div transition:slide class="my-4 bg-white rounded-md shadow-md px-4 py-2">
	<a href="devices/{device.id}" class="font-semibold cursor-pointer">{device.name}</a>
	<p class="text-sm">{device.desc}</p>
</div>
{/each}