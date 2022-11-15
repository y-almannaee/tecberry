<script>
	import Tripanel from '$lib/tripanel.svelte';
	import { page } from '$app/stores';
	let path_arr = [];
	$: path_arr = $page.url.pathname.split('/');
</script>

<Tripanel>
	<svelte:fragment slot="pane">
		<a
			href="/config/devices"
			class:font-semibold={(path_arr.length == 3 && path_arr[2]=="devices") || (path_arr.length>3 && path_arr[3]!="definitions")}
			class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2">Instances</a
		>
		<a
			href="/config/devices/definitions"
			class:font-semibold={path_arr.length>3 && path_arr[3]=="definitions"}
			class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
			>Definitions</a
		>
	</svelte:fragment>
	<svelte:fragment slot="main">
		<div class="m-4">
			<slot />
		</div>
	</svelte:fragment>
</Tripanel>
