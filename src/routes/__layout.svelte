<script lang="ts">
	import '../app.css';
	import { writable } from 'svelte/store';
	const storedTheme = localStorage.getItem('theme');
	const theme = writable(storedTheme);
	theme.subscribe((value) => {
		console.log(value);
		localStorage.setItem('theme', value === 'dark' ? 'dark' : 'light');
		document.documentElement.style.setProperty('--bg', value === 'dark' ? '#011627' : '#eef');
		document.documentElement.style.setProperty('--darks', value === 'dark' ? '#eef' : '#011627');
		document.documentElement.style.setProperty('--main', value === 'dark' ? '#f36' : '#4d6cfa');
		document.documentElement.style.setProperty('--accent', value === 'dark' ? '#4d6cfa' : '#f36');
	});

	function handle_keys(e) {
		if (e.key == ',') {
			theme.update((v) => (v === 'dark' ? 'light' : 'dark'));
		}
	}
</script>

<svelte:window on:keydown={handle_keys} />

<main>
	<slot />
</main>

<footer>
	<p>
		Built with <a href="https://kit.svelte.dev">SvelteKit</a> and
		<a href="https://threejs.org">Three</a>
		<br />©Yaseen AlMannaee, 2022
	</p>
</footer>

<style>
	:global(body) {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}
	footer {
		margin-top: auto;
		justify-content: center;
		align-items: center;
		padding: 40px;
		margin: 0 auto;
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 40px 0;
		}
	}
	@media (max-width: 480px) {
		footer {
			font-size: small;
		}
	}
</style>
