<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { Icon, AtSymbol, DocumentText, Film, Beaker, Code } from 'svelte-hero-icons';
	export const prerender = true;
	let ready = 0;
	let description = '';
	let descriptiontimer = undefined;

	function setdesc(text) {
		if (descriptiontimer) clearTimeout(descriptiontimer);
		description = text;
	}

	function leavedesc() {
		if (descriptiontimer) clearTimeout(descriptiontimer);
		descriptiontimer = setTimeout(() => (description = ''), 500);
	}

	onMount(() => {
		setTimeout(() => {
			ready = 1;
		}),
			500;
	});

	let first_in = { y: 200, delay: 0, opacity: 0, duration: 1200 };
	let first_out = { y: -200, delay: 0, opacity: 0, duration: 1200 };
	let second_in = { y: 200, delay: 1201, opacity: 0, duration: 1200 };
	let second_out = { y: 200, delay: 0, opacity: 0, duration: 1200 };

	$: {
		if (ready == 1) {
			second_in = { y: 200, delay: 1201, opacity: 0, duration: 1200 };
			second_out = { y: 200, delay: 0, opacity: 0, duration: 1200 };
		}
		if (ready == 3) {
			first_in = { y: -200, delay: 0, opacity: 0, duration: 1200 };
			first_out = { y: -200, delay: 0, opacity: 0, duration: 1200 };
		}
	}
</script>

<svelte:head>
	<title>TECBERRY.ml</title>
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

{#if ready == 1}
	<div
		class="w-full h-full flex overflow-hidden text-slate-900"
		in:fly={first_in}
		out:fly={first_out}
	>
		<div class="m-auto mt-32 flex flex-col items-center">
			<img src="/logos/android-chrome-512x512.png" alt="Tecberry Logo" class="  w-24 h-24 mb-2" />
			<h1 class="font-sans font-bold tracking-tighter text-4xl  ">Welcome to TECBERRY</h1>
			<div class="flex gap-8 mt-4">
				<a
					href="https://demo.tecberry.ml/"
					on:mouseover={() => setdesc('See the demo')}
					on:focus={() => setdesc('See the demo')}
					on:mouseleave={() => leavedesc()}
					on:focusout={() => leavedesc()}
					class="hover:text-[#f36] hover:scale-110 will-change-transform duration-300 transition-all"
				>
					<Icon src={Beaker} class="w-10 h-10" />
				</a>
				<div
					on:mouseover={() => setdesc('Watch the presentation<br>Not currently available')}
					on:focus={() => setdesc('Watch the presentation<br>Not currently available')}
					on:mouseleave={() => leavedesc()}
					on:focusout={() => leavedesc()}
					class="hover:text-[#f36] duration-300 transition-all"
				>
					<Icon src={Film} class="text-slate-300 cursor-not-allowed w-10 h-10" />
				</div>
				<a
					href="/tecberry-whitepaper.pdf"
					on:mouseover={() => setdesc('Read the whitepaper')}
					on:focus={() => setdesc('Read the whitepaper')}
					on:mouseleave={() => leavedesc()}
					on:focusout={() => leavedesc()}
					class="hover:text-[#f36] hover:scale-110 will-change-transform duration-300 transition-all"
				>
					<Icon src={DocumentText} class="w-10 h-10" />
				</a>
				<a
					target="_blank"
					rel="noreferrer"
					href="https://github.com/y-almannaee/tecberry"
					on:mouseover={() => setdesc('Contribute to the code')}
					on:focus={() => setdesc('Contribute to the code')}
					on:mouseleave={() => leavedesc()}
					on:focusout={() => leavedesc()}
					class="hover:text-[#f36] hover:scale-110 will-change-transform duration-300 transition-all"
				>
					<Icon src={Code} class="w-10 h-10" />
				</a>
				<button
					on:mouseover={() => setdesc('Get in contact')}
					on:focus={() => setdesc('Get in contact')}
					on:mouseleave={() => leavedesc()}
					on:focusout={() => leavedesc()}
					class="hover:text-[#f36] hover:scale-110 will-change-transform duration-300 transition-all"
					on:click={() => (ready = 2)}
				>
					<Icon src={AtSymbol} class="w-10 h-10" />
				</button>
			</div>
			<div class="flex mt-4 text-center text-slate-700  ">
				<!--Informer-->
				{@html description}
			</div>
		</div>
	</div>
{/if}
{#if ready == 2}
	<div
		class="w-full h-full flex overflow-hidden text-slate-900"
		in:fly={second_in}
		out:fly={second_out}
	>
		<div class="m-auto mt-32 flex flex-col items-center">
			<h1 class="font-sans font-bold tracking-tighter text-4xl  ">Chat with us</h1>
			<div class="flex gap-8 mt-4">
				<div>
					Reach us at <a
						class="underline decoration-1 will-change-transform transition-all decoration-red-300 duration-300 hover:decoration-2 hover:decoration-[#f36]"
						href="mailto:contact@tecberry.ml">contact@tecberry.ml</a
					>
				</div>
			</div>
			<button
				class="mt-4 text-sm text-center text-slate-400"
				on:click={() => {
					ready = 3;
					setTimeout(() => (ready = 1), 1500);
				}}
			>
				Back
			</button>
		</div>
	</div>
{/if}

<style>
	:global(img) {
		user-drag: none;
		-webkit-user-drag: none;
		user-select: none;
		-moz-user-select: none;
		-webkit-user-select: none;
		-ms-user-select: none;
	}

	:global(body) {
		height: 100%;
		width: 100%;
	}
	:global(html) {
		height: 100%;
		width: 100%;
	}
</style>
