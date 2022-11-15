<script>
	/** @type {import('./$types').PageData} */
	export let data;

	let config_type = 0;
</script>

<div class="p-4">
	<h1 class="font-semibold">Scheduler</h1>
	<div
		class="flex place-content-center divide-x-[1px] my-4 bg-white rounded-md shadow-md px-4 py-2"
	>
		<label class="flex px-8"
			><input
				type="radio"
				class="mt-1 mr-2 rounded-full"
				bind:group={config_type}
				value={0}
			/>Simple</label
		>
		<label class="flex px-8"
			><input
				type="radio"
				class="mt-1 mr-2 rounded-full"
				bind:group={config_type}
				value={1}
			/>Advanced</label
		>
	</div>
	<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
		<h2 href="devices/" class="font-semibold">
			{config_type ? 'Advanced configuration' : 'Simple configuration'}
		</h2>
		<div class="text-sm">
			{#if config_type == 0}
				<p>simple</p>
			{:else}
				<p>advanced</p>
			{/if}
		</div>
	</div>
</div>
