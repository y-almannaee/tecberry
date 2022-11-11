<script>
	let data = {};
	data.definitions = [{id: 0, name: "TEC Module", desc: ""}];
	data.devices = [
		{id: 0, name: "Example 1", desc: "An example device"}
	];
	let expanded = false;
</script>

<div class="mx-64 my-6 bg-white rounded-md shadow-md px-4 py-2">
	<h1 class="font-semibold cursor-pointer" on:click={()=>{expanded=!expanded}}>Device definitions</h1>
	{#if expanded}
	
	{#each data.definitions as definition (definition.id)}
	test
	{/each}
	{/if}
</div>
<h1></h1>