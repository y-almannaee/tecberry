<style>
	.page_input {
		position: fixed;
		bottom: 40vh;
		margin: 0 auto;
		font-size: 2.6vh;
		color: var(--darks);
		background-color: transparent;
		border-color: transparent;
		font-family: sans-serif;
		font-weight: 400;
	}
</style>

<script>
	import { blur } from "svelte/transition";

	export let headings, presentation_mode;
	let hidden = true,
		page_input,
		value;

	function handle_keys(e) {
		if (!presentation_mode) return;
		if (hidden == true && e.key == "/") {
			hidden = false;
			e.preventDefault()
		} else if (
			(hidden === false && e.key == "/") ||
			(hidden === false && e.key == "Enter")
		) {
			hidden = true;
			if (value == 0) scroll_to("#title-card");
			else if (!(value > headings.length || value < 0))
				scroll_to(headings[value - 1].getAttribute("href"));
			value = "";
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
</script>

<svelte:window on:keydown="{handle_keys}" />

{#if !hidden}
	<input
		class="page_input"
		type=number
		bind:this="{page_input}"
		transition:blur="{{ duration: 250 }}"
		bind:value
		placeholder="Enter slide number"
		autofocus
	/>
{/if}
