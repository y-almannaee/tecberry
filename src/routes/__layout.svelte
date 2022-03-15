<script lang="ts">
	import '../app.css';
</script>

<main>
	<slot />
</main>

<footer>
	<p>Built with <a href="https://kit.svelte.dev">SvelteKit</a> and <a href="https://threejs.org">Three</a>
	<br>©Yaseen AlMannaee, 2022. Source code GPLv3, code will be released with v1.0</p>
</footer>

<style>
	/*main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 1024px;
		margin: 0 auto;
		box-sizing: border-box;
	}*/
	main {
		font-family: 'Avant Garde', sans-serif;
		text-align: left;
		color: var(--darks);
		padding: 0 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: 80vw;
		}
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 40px;
	}

	footer a {
		font-weight: bold;
	}

	@media (min-width: 480px) {
		footer {
			padding: 40px 0;
		}
	}
</style>
