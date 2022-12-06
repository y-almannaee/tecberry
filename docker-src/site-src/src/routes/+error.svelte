<script>
	import { page } from '$app/stores';
	import { HeartCrack } from 'lucide-svelte';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	let ready = false;
	onMount(() => {
		ready = true;
	});
</script>

<svelte:head>
	<title>Error {$page.error} | TECBERRY.ml</title>
	<meta name="description" value="All about the thermal fatigue testing platform, TECBERRY" />
	<link rel="canonical" href="https://tecberry.ml" />
	<meta property="og:title" content="TECBERRY.ml" />
	<meta property="og:site_name" content="TECBERRY.ml" />
	<meta property="og:url" content="https://tecberry.ml" />
	<meta
		property="og:description"
		content="All about the thermal fatigue testing platform, TECBERRY"
	/>
	<meta property="og:type" content="website" />
	<meta property="og:image" content="https://tecberry.ml/logos/android-chrome-512x512.png" />
</svelte:head>

{#if ready}
	<div class="grid place-items-center h-full" in:fade={{ delay: 230, duration: 900 }}>
		<div class="mb-28 min-w-[80%]">
			<span class="flex"
				><HeartCrack class="relative animate-bounce top-0.5 h-6 w-6" />
				<h1 class="text-2xl pl-1 font-sans font-semibold">Error {$page.status}</h1>
			</span>
			<span class="text-lg">
				Unfortunately, we encountered an error: {$page.error
					? $page.error.message
					: 'Unknown error!'}
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
