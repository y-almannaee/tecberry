<script lang="ts">
	export let presentation_mode;
	$: if (presentation_mode) {
		console.log("Presentation mode");
		document.querySelector(
			"body"
		).style.cursor = `url("../Cur.webp") 16 16, url("../Cur.png") 16 16, pointer`;
	} else {
		console.log("Leaving presentation mode");
		document.querySelector("body").style.cursor = ``;
	}
</script>
