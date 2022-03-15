<style>
	.slide {
		height: 100vh;
		width: 100%;
		overflow: hidden;
	}

	.heading {
		margin-bottom: 24px;
	}

	p {
		font-size: large;
	}

	h2 {
		font-family: "Work Sans", sans-serif;
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
</style>

<script lang="ts">
	export let id_slide,
		short_name,
		capstone = false;
</script>

<div class="slide">
	<span class="heading">
		{#if capstone}
			<h1 id="{id_slide}">
				<a href="{`#${id_slide}`}" bind:this="{short_name}"
					><slot name="slide-title">Untitled slide</slot></a
				>
			</h1>
		{:else}
			<h2 id="{id_slide}">
				<a href="{`#${id_slide}`}" bind:this="{short_name}"
					><slot name="slide-title">Untitled slide</slot></a
				>
			</h2>
		{/if}
		<h3>
			<slot name="byline">
				<!--No byline-->
			</slot>
		</h3>
	</span>
	<slot name="slide-content">Untitled slide</slot>
</div>
