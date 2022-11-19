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
			<div>
				<div class="font-sans font-semibold">Public variables</div>
				<div class="text-xs text-slate-700">
					These variables are accessible by other device instances
				</div>
				{#each data.public as public_var}
					<div />
				{:else}
					<div>No public variables have been declared by this definition</div>
				{/each}
			</div>
		</div>
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
			<div>
				<div class="font-sans font-semibold">Private variables</div>
				<div class="text-xs text-slate-700">
					These variables are only accessible by this device instance
				</div>
				{#each data.private as private_var}
					<div />
				{:else}
					<div>No private variables have been declared by this definition</div>
				{/each}
			</div>
		</div>
	</div>
{/if}
