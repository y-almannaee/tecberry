<script>
	import { slide } from 'svelte/transition';
	import { PackagePlus } from 'lucide-svelte';
	import { tooltip } from '@brainandbones/skeleton';
	let anim = true;

	export let data = {};
</script>

<div>
	<h1 class="font-sans font-semibold">List of device instances</h1>
	<div>The following devices have been instantiated</div>
	<div class="inline-block cursor-pointer" use:tooltip={{content: "Create a new instance", position:'bottom', background: "bg-slate-600", color: "text-slate-100"}}>
		<PackagePlus class="h-6 w-6" />
	</div>
</div>

{#each data.devices as device (device.id)}
	<div transition:slide class="my-4 bg-white rounded-md shadow-md px-4 py-2">
		<a href="devices/{device.id}" class="font-semibold cursor-pointer">{device.name}</a>
		<p class="text-sm">{device.desc}</p>
	</div>
{:else}
	<div>No devices have been instantiated yet!</div>
{/each}
