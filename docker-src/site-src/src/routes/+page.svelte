<script>
	export let data;
	import { page } from '$app/stores';
	import { HeartCrack } from 'lucide-svelte';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	let ready = false;
	onMount(() => {
		ready = true;
	});
</script>

{#if ready}
	<div class="grid place-items-center h-full" in:fade={{ delay: 230, duration: 900 }}>
		<div class="mb-28 min-w-[80%]">
			<span class="flex"
				><HeartCrack class="relative animate-bounce top-0.5 h-6 w-6" />
				<h1 class="text-2xl pl-1 font-sans font-semibold">Can't reach TECBERRY</h1>
			</span>
			<span class="text-lg">
				Unfortunately, the Python backend is not responding.
			</span>
			<span class="block mt-2 text-xs">
				<a class="hover:underline decoration-rose-700 transition-colors duration-300 hover:decoration-2 cursor-pointer" href="/"
					>Go back home?</a
				>
				Alternatively,
				<a
					class="hover:underline decoration-rose-700 transition-colors duration-300 hover:decoration-2 cursor-pointer"
					href="https://github.com/y-almannaee/tecberry/issues"
					>report this error on our issue tracker</a
				>
			</span>
		</div>
	</div>
{/if}
