<script>
	import { onMount } from 'svelte';

	export let headings;
	let first_slide, y, logo, center=false, hidden;
	function get_bearings() {
		if (headings && headings[0] !== undefined) {
			first_slide = headings[0].offsetTop - 25;
		} else {
			center = true;
		}
	}
	onMount(get_bearings);

	$: if (y !== undefined && first_slide !== undefined && y > first_slide) {
		hidden = true;
	} else if (y !== undefined && first_slide !== undefined && y <= first_slide) {
		hidden = false;
	}
</script>

<svelte:window on:resize={get_bearings} bind:scrollY={y} />

<div class="title" class:hidden class:center bind:this={logo} on:click="{()=> { if(!center) document.location="/" }}">
	<h1>TECBERRY.ml</h1>
</div>

<style>
	.title {
		font-family: 'Work Sans', sans-serif;
		font-size: 1.6vh;
		font-weight: 900;
		text-align: right;
		letter-spacing: -1px;
		position: fixed;
		right: 1em;
		margin-right: 0;
		margin-left: auto;
		top: 1em;
		width: fit-content;
		height: fit-content;
		user-select: none;
		cursor: pointer;

		color: transparent;
		transition: background-position 0.2s ease-out, top 0.4s cubic-bezier(0.18, 0.89, 0.02, 1.04),
			font-size 0.1s ease-out;
		background-image: linear-gradient(to right, var(--darks) 50%, var(--accent) 30%);
		background-size: 200% auto;
		background-position: -0% 0;
		background-clip: text;
		-webkit-background-clip: text;
		-moz-background-clip: text;
	}
	.title:hover {
		background-position: -100% 0;
	}
	h1 {
		margin: 0px;
	}
	h1::before {
		content: '';
		background-image: url('/android-chrome-192x192.png');
		background-size: 1em;
		background-repeat: no-repeat;
		width: 1em;
		height: 1em;
		display: inline-block;
		margin-right: 0.1em;
		position: relative;
		top: 0.17em;
	}
	.hidden {
		top: 96.5vh;
		font-size: 1.2vh;
	}
	.hidden h1::before {
		visibility: hidden !important;
	}

	.center {
		position: relative;
		margin: 0;
		padding: 20vh 0 0 17vw;
		font-size: 2.2vh;
		cursor: auto;
	}
	@media (max-width: 640px) {
		.center {
			padding: 4vh 0 0 4vw;
		}
		.hidden {
			visibility: hidden;
		}
	}
</style>
