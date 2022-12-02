<script lang="ts">
	import '../theme.postcss';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../app.css';
	import Logotype from '$lib/logotype.svelte';
	import Dropdown from '$lib/dropdown.svelte';
	import { fade, fly } from 'svelte/transition';
	import { backOut } from 'svelte/easing';
	import { Settings, Menu, X, FileText } from 'lucide-svelte';
	import { navigating, page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { configuration } from '$lib/global_objects';
	import Avatar from '$lib/avatar.svelte';

	let expanded: boolean;

	export let data;

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

	$: if ($navigating) expanded = false;
	$: if (browser && data && data.backend_error && $page.route.id !== '/') goto('/');
	else if (
		browser &&
		data &&
		data.loggedIn !== undefined &&
		!data.loggedIn &&
		$page.route.id !== '/login'
	)
		goto('/login');
</script>

{#if $configuration && $configuration.dnt!== undefined && !$configuration.dnt}
	<noscript>
		<img
			src="https://shnt.yaseen.ae/ingress/473beb52-2a5e-458a-aa20-dc0b07e9441d/pixel.gif"
			alt="shnt"
		/>
	</noscript>
	<script
		defer
		src="https://shnt.yaseen.ae/ingress/473beb52-2a5e-458a-aa20-dc0b07e9441d/script.js"
	></script>
{/if}

<div class="flex flex-col h-screen justify-between" data-sveltekit-prefetch>
	<header
		class="text-lg py-2 fixed w-screen top-0 z-20 gap-2 items-center px-2 bg-white dark:bg-slate-800 shadow-md hidden md:flex text-slate-900 dark:text-slate-200"
	>
		<Logotype class="text-lg" />
		{#each links as link (link.id)}
			<Dropdown
				links={link.to}
				disabled={!(data && data.loggedIn)}
				links_class={'text-base top-10 -mt-10 pt-10'}
			>
				<svelte:fragment slot="title">{link.text}</svelte:fragment>
			</Dropdown>
		{/each}
		<a
			on:click={(e) => {
				if (data && !data.loggedIn) {
					e.preventDefault();
				}
			}}
			class:cursor-not-allowed={!(data && data.loggedIn)}
			href="/documentation"
			class="transition-colors duration-300 decoration-rose-700 dark:decoration-sky-500 font-sans"
			>Docs</a
		>
		<a
			on:click={(e) => {
				if (data && !data.loggedIn) {
					e.preventDefault();
				}
			}}
			class:cursor-not-allowed={!(data && data.loggedIn)}
			href="/settings/account"
			class="ml-auto"
			><Settings class="h-6 transition-colors duration-300 hover:text-[#f36] rounded" /></a
		>
		<Avatar userdata={data} classes="mr-2" classes_icon="h-6" />
	</header>
	<header
		class="text-lg will-change-transform fixed w-screen top-0 z-20 flex gap-8 items-center lg:p-2 p-0.5 bg-white dark:bg-slate-800 shadow-md md:hidden text-slate-900"
	>
		<Logotype class="lg:text-3xl text-lg ml-2" />
		<button
			class="ml-auto"
			on:click={() => {
				expanded = !expanded;
			}}><Menu class="h-8 mr-2 transition-colors duration-300 hover:text-[#f36] rounded" /></button
		>
		{#if expanded}
			<div
				class="bg-slate-500/40 text-sm lg:text-base backdrop-blur-sm dark:bg-slate-800/40 fixed top-0 left-0 w-screen h-screen text-slate-900 dark:text-slate-200"
				transition:fade
				on:click|self={() => {
					expanded = false;
				}}
				on:keypress|self={() => {
					expanded = false;
				}}
			>
				<div
					transition:fly={{ easing: backOut, duration: 400, y: 50, opacity: 0 }}
					class="mx-auto max-w-xs p-4 rounded will-change-transform bg-white shadow-xl dark:bg-slate-800 mt-4 lg:mt-16"
				>
					<button
						class="absolute top-5 right-4"
						on:click={() => {
							expanded = false;
						}}
						on:keypress|self={() => {
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
									on:click={(e) => {
										if (data && !data.loggedIn) {
											e.preventDefault();
										}
									}}
									class:cursor-not-allowed={!(data && data.loggedIn)}
									href={a.href}
									class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2 font-light text-sm lg:text-lg"
									>{a.text}</a
								>
							{/each}
						</div>
					{/each}
					<div class="p-1 flex space-x-2 justify-center items-center">
						<a
							on:click={(e) => {
								if (data && !data.loggedIn) {
									e.preventDefault();
								}
							}}
							class:cursor-not-allowed={!(data && data.loggedIn)}
							href="/documentation"
							class="mr-auto"
							><FileText class="h-8 transition-colors duration-300 hover:text-[#f36] rounded" /></a
						>
						<a
							on:click={(e) => {
								if (data && !data.loggedIn) {
									e.preventDefault();
								}
							}}
							class:cursor-not-allowed={!(data && data.loggedIn)}
							href="/settings/account"
							><Settings class="h-8 transition-colors duration-300 hover:text-[#f36] rounded" /></a
						>
						<Avatar userdata={data} classes_icon="h-7 m-auto" />
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
