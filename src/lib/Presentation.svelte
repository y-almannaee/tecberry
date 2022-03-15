<script lang="ts">
	export let presentation_mode;
	import { browser } from "$app/env";
	$: if (browser) if (presentation_mode) {
		console.log("Presentation mode");
		document.querySelector(
			"body"
		).style.cursor = `url("../Cursor.png"), pointer`;
	} else {
		console.log("Leaving presentation mode");
		document.querySelector("body").style.cursor = ``;
	}
</script>
