<style>
	/* work-sans-700 - latin */
	@font-face {
		font-family: "Work Sans";
		font-style: normal;
		font-weight: 700;
		src: url("../fonts/work-sans-v16-latin-700.eot"); /* IE9 Compat Modes */
		src: local(""),
			url("../fonts/work-sans-v16-latin-700.eot?#iefix")
				format("embedded-opentype"),
			/* IE6-IE8 */ url("../fonts/work-sans-v16-latin-700.woff2")
				format("woff2"),
			/* Super Modern Browsers */ url("../fonts/work-sans-v16-latin-700.woff")
				format("woff"),
			/* Modern Browsers */ url("../fonts/work-sans-v16-latin-700.ttf")
				format("truetype"),
			/* Safari, Android, iOS */
				url("../fonts/work-sans-v16-latin-700.svg#WorkSans") format("svg"); /* Legacy iOS */
	}

	/* work-sans-900 - latin */
	@font-face {
		font-family: "Work Sans";
		font-style: normal;
		font-weight: 900;
		src: url("../fonts/work-sans-v16-latin-900.eot"); /* IE9 Compat Modes */
		src: local(""),
			url("../fonts/work-sans-v16-latin-900.eot?#iefix")
				format("embedded-opentype"),
			/* IE6-IE8 */ url("../fonts/work-sans-v16-latin-900.woff2")
				format("woff2"),
			/* Super Modern Browsers */ url("../fonts/work-sans-v16-latin-900.woff")
				format("woff"),
			/* Modern Browsers */ url("../fonts/work-sans-v16-latin-900.ttf")
				format("truetype"),
			/* Safari, Android, iOS */
				url("../fonts/work-sans-v16-latin-900.svg#WorkSans") format("svg"); /* Legacy iOS */
	}

	:global(body) {
		background-color: #eef;
	}

	:global(::selection) {
		background: #4d6cfa;
		color: #eef;
	}

	main {
		font-family: "Avant Garde", sans-serif;
		text-align: left;
		padding: 0 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3366;
		font-size: xx-large;
		font-weight: 100;
	}

	h1 {
		font-family: "Work Sans", sans-serif;
		text-transform: uppercase;
		line-height: 1em;
		margin-bottom: 0.2em;
		padding-top: 18px;
		margin-top: 0;
	}

	h3 {
		display: inline;
		font-size: larger;
		font-weight: 400;
	}

	h3:after {
		content: "\a";
		white-space: pre;
	}

	.slide {
		height: 100vh;
		width: 100%;
	}

	@media (min-width: 640px) {
		main {
			max-width: 80vw;
		}
	}
</style>

<script lang="ts">
	import { onMount } from "svelte";
	import { debounce } from "lodash";
	import Slide from "./Slide.svelte";
	import HelloCube from "./HelloCube.svelte";
	import Presentation from "./Presentation.svelte";
	import Logo from "./Logo.svelte";

	let y = 0;
	let headings = [];
	let presentation_mode, shared_style;
	let waited = false;

	onMount(() => {
		const location = window.location.toString().split("#")[1];
		if (location !== undefined) {
			scroll_to(location);
		} else {
			scroll_to("title-card");
		}
		waited = true;
	});

	function handle_keys(e) {
		if (e.key == "ArrowRight" || e.key == "ArrowDown" || e.key == " ") {
			e.preventDefault();
			const location = window.location.toString().split("#")[1];
			if (location !== undefined) {
				for (let i = 0; i < headings.length; i++) {
					if (`#${location}` === headings[i].getAttribute("href")) {
						if (i + 1 !== headings.length)
							scroll_to(headings[i + 1].getAttribute("href"));
						break;
					}
				}
			} else {
				scroll_to(headings[0].getAttribute("href"));
			}
		} else if (e.key == "ArrowLeft" || e.key == "ArrowUp") {
			e.preventDefault();
			const location = window.location.toString().split("#")[1];
			if (location !== undefined) {
				for (let i = 0; i < headings.length; i++) {
					if (`#${location}` === headings[i].getAttribute("href")) {
						if (i - 1 === -1) scroll_to("title-card");
						else scroll_to(headings[i - 1].getAttribute("href"));
						break;
					}
				}
			} else {
				scroll_to("title-card");
			}
		} else if (e.key == ".") {
			presentation_mode = presentation_mode ? false : true;
		}
	}

	function scroll_to(target) {
		target = target.toString().startsWith("#")
			? target.toString()
			: `#${target.toString()}`;
		const el = document.querySelector(target);
		if (!el) return;
		el.scrollIntoView({
			behavior: "smooth",
		});
	}

	function replace_hash(new_hash: string) {
		const location = window.location.toString().split("#");
		if (location[1] !== undefined && location[1] !== new_hash.replace("#", ""))
			history.replaceState(null, null, location[0] + new_hash);
		else if (location[1] === undefined && new_hash !== "")
			history.replaceState(null, null, location[0] + new_hash);
	}
	$: if (waited) {
		if (y < 100) {
			replace_hash("");
		} else {
			for (let i = 0; i < headings.length; i++) {
				if (headings[i].offsetTop < y + 50 && headings[i].offsetTop > y - 50) {
					const heading = headings[i].getAttribute("href");
					replace_hash(heading);
					break;
				}
			}
		}
	}
</script>

<svelte:window on:keydown="{handle_keys}" bind:scrollY="{y}" />

<Logo />
<main>
	<Presentation bind:presentation_mode />
	<div class="slide">
		<span class="heading">
			<h1 id="title-card">
				TEC modules for rapid and automated thermomechanical fatigue testing
			</h1>
			<h3>
				By Maryam K, Mohammed A, and Yaseen A <br /> Advised by Dr. Maen Alkhader
			</h3>
		</span>
		<p>The introduction goes here.</p>
	</div>
	<Slide id_slide="what-is-a-tec" bind:short_name="{headings[headings.length]}">
		<svelte:fragment slot="slide-title">What is a TEC module?</svelte:fragment>
		<svelte:fragment slot="slide-content">
			<p>
				A TEC module, also known as a thermoelectric, or a Peltier module, is
				basically a heat pump.
			</p>
		</svelte:fragment>
	</Slide>
	<Slide id_slide="our-idea" bind:short_name="{headings[headings.length]}">
		<svelte:fragment slot="slide-title">Our Idea</svelte:fragment>
		<svelte:fragment slot="slide-content">
			<p>
				Our idea is to use a bunch to heat and cool stuff to see if it breaks
			</p>
		</svelte:fragment>
	</Slide>
	<HelloCube />
</main>
