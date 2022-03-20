<script lang="ts">
	import { onMount } from 'svelte';

	export let id_slide,
		short_name,
		center = false,
		highlighted = false,
		capstone = false;

	let highlight_count = 0;

	function highlight_new() {
		let highlight = document.getElementsByClassName('highlighted')[highlight_count++];
		if (highlight !== undefined) {
			highlight.style.backgroundPosition = '-99.99% 0';
		setTimeout(highlight_new, 300);
		}
	}
	onMount(() => {
		setTimeout(highlight_new, 1500);
	});
</script>

<div class="slide">
	<span class="heading">
		{#if capstone}
			<a href={`#${id_slide}`} bind:this={short_name}
				><h1 id={id_slide} class:center class:highlighted>
					<slot name="slide-title">Untitled slide</slot>
				</h1></a
			>
		{:else}
			<a href={`#${id_slide}`} bind:this={short_name}
				><h2 id={id_slide}>
					<slot name="slide-title">Untitled slide</slot>
				</h2></a
			>
		{/if}
		<h3 class:highlighted>
			<slot name="byline">
				<!--No byline-->
			</slot>
		</h3>
	</span>
	<slot name="slide-content"></slot>
</div>

<style>
	.slide {
		height: 100vh;
		width: fit-content;
		overflow: hidden;
		margin: 2vw;
	}

	.heading {
		margin-bottom: 24px;
	}

	h2 {
		font-family: 'Work Sans', sans-serif;
		font-weight: 700;
		text-transform: uppercase;
		line-height: 1em;
		margin-bottom: 0.2em;
		padding-top: 18px;
		margin-top: 0;
	}

	h1 {
		color: var(--accent);
		font-size: 3rem;
		font-weight: 900;
		font-family: 'Work Sans', sans-serif;
		text-transform: uppercase;
		line-height: 1em;
		margin-bottom: 0.2em;
		padding-top: 18px;
		margin-top: 0;
	}

	h3 {
		display: inline;
		font-size: 2rem;
		font-weight: 400;
	}

	h3:after {
		content: '\a';
		white-space: pre;
	}

	/* h2 a,
	h1 a {
		all: inherit;
		cursor: pointer;
	} */

	h1:empty,
	h2:empty,
	h3:empty {
		display: none;
	}

	h2 {
		font-size: 2.7rem;
	}

	.center {
		padding-top: 8vh;
	}
	.highlighted {
		color: var(--bg);
		transition: background-position 1.7s cubic-bezier(0.95, 0.05, 0.35, 1.01);
		background-image: linear-gradient(to right, transparent 50%, var(--accent) 30%);
		background-size: 200% auto;
		background-position: -0% 0;
		background-clip: content-box;
		-moz-background-clip: content-box;
		-webkit-background-clip: content-box;
	}

</style>
