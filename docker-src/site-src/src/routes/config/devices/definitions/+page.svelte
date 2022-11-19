<script>
	import {slide} from 'svelte/transition';
	let anim = true;

	let data = {};
	data.definitions = [
		{id: 0, name: "Example", desc: "An example definition"},
		{id: 1, name: "Example", desc: "An example definition"},
		{id: 2, name: "Example", desc: "An example definition"},
		{id: 3, name: "Example", desc: "An example definition"},
		{id: 4, name: "Example", desc: "An example definition"},
		{id: 5, name: "Example", desc: "An example definition"},
		{id: 6, name: "Example", desc: "An example definition"},
		{id: 7, name: "Example", desc: "An example definition"},
	];
</script>

{#each data.definitions as definition (definition.id)}
<div transition:slide class="my-4 bg-white rounded-md shadow-md px-4 py-2">
	<a href="definitions/{definition.id}" class="font-semibold cursor-pointer">{definition.name}</a>
	<p class="text-sm">{definition.desc}</p>
</div>
{/each}