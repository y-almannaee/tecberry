<script lang="ts">
	export const prerender = true;
	import '../theme.postcss';
	import '@brainandbones/skeleton/styles/all.css';
	import '../app.css';
	import Logotype from '$lib/logotype.svelte';
	import Dropdown from '$lib/dropdown.svelte';
	import { fade, fly } from 'svelte/transition';
	import { backOut } from 'svelte/easing';
	import { LogIn, Settings, Menu, X, FileText } from 'lucide-svelte';

	let expanded: boolean;

	const links = [
		{
			id: 0,
			text: 'Statistics & Data',
			to: [
				{ href: '/stats/insight', text: 'Insight' },
				{ href: '/stats/logs', text: 'Logs' }
			]
		},
		{
			id: 1,
			text: 'Configuration',
			to: [
				{ href: '/config/scheduler', text: 'Scheduler' },
				{ href: '/config/devices', text: 'Devices' }
			]
		}
	];
</script>

<div class="flex flex-col h-screen justify-between" data-sveltekit-prefetch>
	<header
		class="text-lg py-2 sticky top-0 z-20 gap-2 items-center px-2 bg-white dark:bg-slate-800 shadow-md hidden md:flex text-slate-900 dark:text-slate-200"
	>
		<Logotype class="text-lg" />
		{#each links as link (link.id)}
			<Dropdown links={link.to} links_class={'text-base top-10 -mt-10 pt-10'}>
				<svelte:fragment slot="title">{link.text}</svelte:fragment>
			</Dropdown>
		{/each}
		<a
			href="/documentation"
			class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2 font-sans">Docs</a
		>
		<a href="/settings/account" class="ml-auto"
			><Settings class="h-6 transition-colors duration-300 hover:text-[#f36] rounded" /></a
		>
		<a href="/login" class="mr-4"
			><LogIn class="h-6 transition-colors duration-300 hover:text-[#f36] rounded" /></a
		>
	</header>
	<header
		class="text-lg will-change-transform sticky top-0 z-20 flex gap-8 items-center lg:p-2 p-0.5 bg-white dark:bg-slate-800 shadow-md md:hidden text-slate-900"
	>
		<Logotype class="lg:text-3xl text-lg" />
		<button
			class="ml-auto"
			on:click={() => {
				expanded = !expanded;
			}}><Menu class="h-8 transition-colors duration-300 hover:text-[#f36] rounded" /></button
		>
		{#if expanded}
			<div
				class="bg-slate-500/40 text-sm lg:text-base backdrop-blur-sm dark:bg-slate-800/40 fixed top-0 left-0 w-screen h-screen text-slate-900 dark:text-slate-200"
				transition:fade
				on:click|self={() => {
					expanded = false;
				}}
			>
				<div
					transition:fly={{ easing: backOut, duration: 400, y: 50, opacity: 0 }}
					class="mx-auto max-w-xs p-4 rounded will-change-transform bg-white shadow-xl dark:bg-slate-800 mt-16"
				>
					<button
						class="absolute top-5 right-4"
						on:click={() => {
							expanded = false;
						}}
					>
						<X class="h-5 transition-colors duration-300 hover:text-[#f36] rounded" />
					</button>
					{#each links as link (link.id)}
						<h1 class="font-semibold cursor-default">{link.text}</h1>
						<div class="flex-col flex pl-4 pb-2 mb-2 border-b rounded">
							{#each link.to as a}
								<a
									on:click={() => (expanded = false)}
									href={a.href}
									class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2 font-light text-sm lg:text-lg"
									>{a.text}</a
								>
							{/each}
						</div>
					{/each}
					<div class="p-1 flex space-x-2">
						<a on:click={() => (expanded = false)} href="/documentation" class="mr-auto"
							><FileText class="h-8 transition-colors duration-300 hover:text-[#f36] rounded" /></a
						>
						<a on:click={() => (expanded = false)} href="/settings/account"
							><Settings class="h-8 transition-colors duration-300 hover:text-[#f36] rounded" /></a
						>
						<a on:click={() => (expanded = false)} href="/login"
							><LogIn class="h-8 transition-colors duration-300 hover:text-[#f36] rounded" /></a
						>
					</div>
				</div>
			</div>
		{/if}
	</header>
	<main id="main_parent" class="mb-auto flex-1">
		<slot />
	</main>
	<footer />
</div>
