<script context="module" lang="ts">
	export const prerender = true;
</script>

<script lang="ts">
	let headings = undefined;
	import Logo from '$lib/Logo.svelte';
</script>

<svelte:head>
	<title>TECBERRY.ml</title>
    <meta name="description" content="TECBERRY.ml | TECnology" />
</svelte:head>

<Logo bind:headings />

<section>
	<div>
		<h1><a href="/presentation/1">Design Presentation 1</a></h1>
		<span class="tooltip" style="visibility:hidden">Placeholder</span>
	</div>
	<div>
		<h1><a class="disabled">Design Presentation 2</a></h1>
		<span class="tooltip">It's still Spring semester 😅</span>
	</div>
	<div>
		<h1><a class="disabled">TECBERRY Online Demo</a></h1>
		<span class="tooltip">Soon</span>
	</div>
	<div>
		<h1><a class="disabled">TECBERRY Setup</a></h1>
		<span class="tooltip">Coming this Fall</span>
	</div>
	<div>
		<h1><a class="disabled">Source code</a></h1>
		<span class="tooltip">Coming very soon</span>
	</div>
</section>

<style>
	section {
		margin: 6vh auto 0 16vw;
		min-height: 48vh;
	}
	h1 {
		color: var(--accent);
		font-size: xx-large;
		font-weight: 900;
		font-family: 'Work Sans', sans-serif;
		text-transform: uppercase;
		line-height: 1em;
		margin-bottom: 24px;
		margin-top: 0;
	}
	h1 a {
		all: inherit;
		cursor: pointer;
	}

	div {
		position: relative;
		max-width: fit-content;
	}

	.tooltip {
		font-family: 'Avant Garde', sans-serif;
		visibility: hidden;
		width: 220px;
		background-color: var(--accent);
		opacity: 80%;
		color: var(--bg);
		padding: 5px 6px;
		position: absolute;
		z-index: 1;
		border-radius: 6px;
		text-align: center;
		top: -5px;
		left: 105%;
		pointer-events: none;
	}

	.tooltip:before {
		content: ' ';
		display: block;
		position: absolute;
		left: -4px;
		top: 8px;
		width: 14px;
		height: 14px;
		background-color: var(--accent);
		z-index: -1;
		transform: rotate(45deg);
		-webkit-transform: rotate(45deg);
		-moz-transform: rotate(45deg);
	}

	@media (max-width: 640px) {
		.tooltip {
			position: relative;
			margin-left: 48px;
			left:0px;
			top:0px;
		}
		.tooltip:before {
			top: 0px;
			left: -2px;
			transform: rotate(10deg) skew(25deg);
			-webkit-transform: rotate(10deg) skew(25deg);
			-moz-transform: rotate(10deg) skew(25deg);
		}
		section {
			margin: 6vh 0;
		}
		h1 {
			margin: 10px 0 4px 0;
		}
	}

	h1:hover + .tooltip {
		visibility: visible;
	}

	a.disabled {
		opacity: 45%;
		color: #ff3366;
		cursor: not-allowed;
		user-select: none;
	}
</style>
