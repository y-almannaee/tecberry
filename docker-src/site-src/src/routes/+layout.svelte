<script lang="ts">
	export const prerender = true;
	import '../app.css';
	import Logotype from '$lib/logotype.svelte';
	import Dropdown from '$lib/dropdown.svelte';
	import { fade, fly } from 'svelte/transition';
	import { backOut } from 'svelte/easing';
	import { LogIn, Settings, Menu, X } from 'lucide-svelte';

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
				{ href: '/config/program', text: 'Program' },
				{ href: '/config/wiring', text: 'Wiring' }
			]
		}
	];
</script>

<div class="flex flex-col h-screen justify-between">
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
			class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2">Docs</a
		>
		<a href="/settings/account" class="ml-auto"
			><Settings class="h-6 transition-colors duration-300 hover:text-[#f36] rounded" /></a
		>
		<a href="/login" class="mr-4"><LogIn class="h-6 transition-colors duration-300 hover:text-[#f36] rounded" /></a>
	</header>
	<header
		class="text-lg will-change-transform sticky top-0 z-20 flex gap-8 items-center p-2 bg-white dark:bg-slate-800 shadow-md md:hidden text-slate-900">
		<Logotype class="text-3xl" />
		<button
			class="ml-auto"
			on:click={() => {
				expanded = !expanded;
			}}
			><Menu
				class="h-8 transition-colors duration-300 hover:text-[#f36] rounded" /></button>
		{#if expanded}
			<div
				class="bg-slate-500/40 backdrop-blur-sm dark:bg-slate-800/40 fixed top-0 left-0 w-screen h-screen text-slate-900 dark:text-slate-200"
				transition:fade
				on:click|self={() => {
					expanded = false;
				}}>
				<div
					transition:fly={{ easing: backOut, duration: 400, y: 50, opacity: 0 }}
					class="mx-auto max-w-xs p-4 rounded will-change-transform bg-white dark:bg-slate-800 mt-16">
					<button
						class="absolute top-5 right-4"
						on:click={() => {
							expanded = false;
						}}>
						<X
							class="h-5 transition-colors duration-300 hover:text-[#f36] rounded" />
					</button>
					{#each links as link (link.id)}
						<h1 class="font-semibold">{link.text}</h1>
						<div class="flex-col flex pl-4 pb-2 mb-2 border-b rounded">
							{#each link.to as a}
								<a
									href={a.href}
									class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2 font-light text-lg"
									>{a.text}</a>
							{/each}
						</div>
					{/each}
				</div>
			</div>
		{/if}
	</header>
	<main id="main_parent" class="mb-auto flex-1">
		<slot />
	</main>
	<footer>

	</footer>
</div>