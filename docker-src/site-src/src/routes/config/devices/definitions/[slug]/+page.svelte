<script>
	/** @type {import('./$types').PageData} */
	export let data;
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { expoIn } from 'svelte/easing';

	let ready = false;
	onMount(() => (ready = true));
</script>

{#if ready}
	<div in:fly={{ duration: 300, y: 200, opacity: 0, easing: expoIn }}>
		<h1 class="font-sans font-semibold">{data.name}</h1>
		<div>{data.desc}</div>
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
			<label>
				<div class="font-sans font-semibold">List of public variables</div>
				<div class="text-xs text-slate-700">These variables will be accessible by other instances, takes a comma-separated list of variables to expose</div>
				<input class='mt-2 rounded-md' placeholder="x,y,temperature,humidity" type="text">
			</label>
		</div>
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
			<label>
				<div class="font-sans font-semibold">List of private variables</div>
				<div class="text-xs text-slate-700">These variables will be assigned by someone who is instantiating this definition, but they won't be accessible by other instances, takes a comma-separated list of variables to expose</div>
				<input class='mt-2 rounded-md' placeholder="pin_data,address,secret_value" type="text">
			</label>
		</div>
	</div>
{/if}
