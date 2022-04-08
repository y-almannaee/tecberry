<script lang="ts">
	import "../app.css";
	import Logotype from "$lib/logotype.svelte";
	import Dropdown from "$lib/dropdown.svelte";
	import { fade, fly } from "svelte/transition";
	import { backOut } from "svelte/easing";
	import { Icon } from "@steeze-ui/svelte-icon";
	import { Login, Cog, Menu, X } from "@steeze-ui/heroicons";

	let expanded: boolean = true,
		scrollY,
		moved_down;

	const links = [
		{
			id: 0,
			text: "Statistics",
			to: [
				{ href: "/stats/realtime", text: "Realtime" },
				{ href: "/stats/logs", text: "Logs" }
			]
		},
		{
			id: 1,
			text: "Configuration",
			to: [
				{ href: "/config/curve", text: "Curve" },
				{ href: "/config/pi", text: "Raspberry Pi" }
			]
		}
	];

	$: if (scrollY > 40) {
		moved_down = true;
	} else if (scrollY < 10) {
		moved_down = false;
	}
</script>

<svelte:window bind:scrollY />

<div class="flex flex-col h-screen justify-between">
	<header
		class="{moved_down
			? 'text-lg py-2'
			: 'text-2xl py-4'} transition-all will-change-transform sticky top-0 z-20 gap-2 items-center px-2 bg-white dark:bg-slate-800 shadow-md hidden md:flex text-slate-900 dark:text-slate-200">
		<Logotype class="{moved_down ? 'text-lg' : 'text-3xl'} transition-all duration-300" />
		{#each links as link (link.id)}
			<Dropdown
				links={link.to}
				links_class={moved_down ? "text-base top-10 -mt-10 pt-10" : "text-lg top-14 -mt-14 pt-14"}>
				<svelte:fragment slot="title">{link.text}</svelte:fragment>
			</Dropdown>
		{/each}
		<a
			href="/documentation"
			class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2">Docs</a>
		<a href="/settings/account" class="ml-auto"
			><Icon
				src={Cog}
				theme="solid"
				class="{moved_down
					? 'h-6'
					: 'h-8'} transition-all duration-300 hover:text-[#f36] rounded" /></a>
		<a href="/login" class="mr-4"
			><Icon
				src={Login}
				theme="outline"
				class="-scale-x-100 {moved_down
					? 'h-6'
					: 'h-8'} transition-all duration-300 hover:text-[#f36] rounded" /></a>
	</header>
	<header
		class="{moved_down
			? 'text-lg'
			: 'text-2xl'} transition-all will-change-transform sticky top-0 z-20 flex gap-8 items-center p-2 bg-white dark:bg-slate-800 shadow-md md:hidden text-slate-900">
		<Logotype class="text-3xl" />
		<button
			class="ml-auto"
			on:click={() => {
				expanded = !expanded;
			}}
			><Icon
				src={Menu}
				theme="outline"
				class="h-8 transition-all duration-300 hover:text-[#f36] rounded" /></button>
		{#if expanded}
			<div
				class="bg-slate-500/40 dark:bg-slate-800/40 fixed top-0 left-0 w-screen h-screen text-slate-900 dark:text-slate-200"
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
						<Icon
							src={X}
							theme="outline"
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
	<main class="mb-auto" style="min-height: calc(100% - 96px - 70px)">
		<slot />
	</main>
	<footer class="bg-white dark:bg-slate-800 shadow-2xl w-full z-10 relative">
		<div class="p-4 mx-auto md:p-6">
			<span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">
				© 2022 <a
					href="https://yaseen.ae"
					class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
					>Yaseen AlMannaee</a>
				<br /> Built with
				<a
					class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
					href="https://kit.svelte.dev">
					SvelteKit
				</a>
				and
				<a
					class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
					href="https://tailwindcss.com">TailwindCSS</a>
			</span>
		</div>
		<!-- <ul class="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0">
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6 ">About</a>
				</li>
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6">Privacy Policy</a>
				</li>
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6">Licensing</a>
				</li>
				<li>
					<a href="#" class="hover:underline">Contact</a>
				</li>
			</ul> -->
	</footer>
</div>
