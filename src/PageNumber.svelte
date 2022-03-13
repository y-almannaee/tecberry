<style>
	.hidden {
		visibility: hidden;
	}
	.page_number {
		position: fixed;
		bottom: 1em;
		left: 1em;
		font-size: 2.6vh;
		color: var(--darks);
		opacity: 65%;
		font-family: sans-serif;
		font-weight: 400;
	}
</style>

<script>
	import { blur, fly } from "svelte/transition";

	export let headings, presentation_mode;
	let y,
		hidden = true,
		page_number,
		page = 0;

	$: if (presentation_mode) {
		for (let i = 0; i < headings.length; i++) {
			if (headings[i].offsetTop > y - 25 && headings[i].offsetTop < y + 25) {
				page = i + 1;
				hidden = false;
				break;
			} else if (y - 25 < headings[0].offsetTop) {
				hidden = true;
				break;
			}
		}
	} else hidden = true;
</script>

<svelte:window bind:scrollY="{y}" />

{#key page}
	<div
		class="page_number"
		class:hidden
		bind:this="{page_number}"
		in:fly="{{ x: -200, duration: 300 }}"
		out:blur="{{ duration: 250 }}"
	>
		{page}
	</div>
{/key}
