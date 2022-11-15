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
		<h1 class="font-semibold">{data.name}</h1>
		<div>{data.desc}</div>
	</div>
{/if}
