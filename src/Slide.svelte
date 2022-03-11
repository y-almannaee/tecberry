<style>
	.slide {
		height: 100vh;
		width: 100%;
	}

	.heading {
		margin-bottom: 24px;
	}

	p {
		font-size: large;
	}

	h2 {
		font-family: "Work Sans", sans-serif;
		text-transform: uppercase;
		line-height: 1em;
		margin-bottom: 0.2em;
		padding-top: 18px;
		margin-top: 0;
	}

	h2 a {
		all: inherit;
	}

	h2 {
		font-size: x-large;
	}
</style>

<script lang="ts">
	export let id_slide;
	export let short_name;
</script>

<div class="slide">
	<span class="heading">
		<h2 id="{id_slide}">
			<a href="{`#${id_slide}`}" bind:this={short_name}><slot name="slide-title">Untitled slide</slot></a>
		</h2>
	</span>
	<slot name="slide-content">Untitled slide</slot>
</div>
