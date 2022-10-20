<script>
	import { browser } from "$app/environment";
</script>
<div class="title">
	<h1 {...$$restProps} style="color:transparent !important">
		TECBERRY{(() => {
			if (browser && location.hostname === "tecberry.ml" || browser && location.hostname === "demo.tecberry.ml")
				return ".ml";
			else return "";
		})()}
	</h1>
</div>

<style>
	.title {
		font-family: "Work Sans", sans-serif;
		font-weight: 900;
		text-align: right;
		letter-spacing: -1px;
		width: fit-content;
		height: fit-content;
		user-select: none;
		cursor: pointer;

		color: transparent;
		transition: background-position 0.2s ease-out;
		background-image: linear-gradient(
			to left,
			#f36 50%,
			var(--color-slate-900) 30%
		);
		background-size: 200% auto;
		background-position: -0% 0;
		background-clip: text;
		-webkit-background-clip: text;
		-moz-background-clip: text;
	}
	:global(.dark .title) {
		background-image: linear-gradient(
			to left,
			#f36 50%,
			var(--color-slate-200) 30%
		) !important;
	}
	.title:hover {
		background-position: -100% 0;
	}
	h1 {
		margin: 0px;
	}
	h1::before {
		content: "";
		background-image: url("/logos/android-chrome-192x192.png");
		background-size: 1em;
		background-repeat: no-repeat;
		width: 1em;
		height: 1em;
		display: inline-block;
		margin-right: 0.1em;
		position: relative;
		top: 0.17em;
	}
</style>
