<script lang="ts">
	import { onMount } from 'svelte';

	export let id_slide,
		short_name,
		center = false,
		highlighted = false,
		capstone = false;

	let highlight_init = false;
	onMount(() => {
		setTimeout(() => {
			highlight_init = true;
		}, 1500);
	});
</script>

<div class="slide">
	<span class="heading">
		{#if capstone}
			<a href={`#${id_slide}`} bind:this={short_name}
				><h1 id={id_slide} class:center class:highlighted class:highlight_init>
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
		<h3 class:highlight_init class:highlighted>
			<slot name="byline">
				<!--No byline-->
			</slot>
		</h3>
	</span>
	<slot name="slide-content">Untitled slide</slot>
</div>

<style>
	.slide {
		height: 100vh;
		width: 100%;
		overflow: visible;
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
		font-size: xx-large;
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
		font-size: larger;
		font-weight: 400;
	}

	h3:after {
		content: '\a';
		white-space: pre;
	}

	h2 a,
	h1 a {
		all: inherit;
		cursor: pointer;
	}

	h1:empty,
	h2:empty,
	h3:empty {
		display: none;
	}

	h2 {
		font-size: x-large;
	}

	.center {
		padding-top: 8vh;
	}
	.highlighted {
		color: var(--bg);
		transition: background-position 1.7s cubic-bezier(.95,.05,.35,1.01);
		background-image: linear-gradient(to right, transparent 50%, var(--accent) 30%);
		background-size: 200% auto;
		background-position: -0% 0;
		background-clip: content-box;
		-moz-background-clip: content-box;
		-webkit-background-clip: content-box;
	}
	.highlight_init {
		background-position: -99.99% 0;
	}
</style>
