<script>
	import { slide } from 'svelte/transition';
	import { PackagePlus } from 'lucide-svelte';
	import { tooltip, Modal, modalStore } from '@skeletonlabs/skeleton';
	import { backend_url } from '$lib/global_objects';
	import { invalidate } from '$app/navigation';
	let anim = true;

	export let data;
	function modal() {
		const confirm = {
			type: 'prompt',
			title: 'Enter device name',
			body: 'Please provide a recognizable name for your device',
			response: async (r) => {
				if (r == false) return;
				let backend = backend_url('/devices');
				const res = await fetch(backend, { method: 'POST', body: JSON.stringify({ name: r }) });
				invalidate((url) => true);
			}
		};
		modalStore.trigger(confirm);
	}
</script>

<svelte:head> 
	<title>Devices | TECBERRY.ml</title>
</svelte:head>

<Modal
	regionBackdrop="bg-backdrop-token backdrop-blur-sm"
	on:keydown={(e) => {
		if (e.key == 'Enter') document.querySelector('.btn-filled-primary').click();
	}}
/>
<div>
	<h1 class="font-sans font-semibold">List of device instances</h1>
	<div>The following devices have been instantiated</div>
	<div
		class="inline-block cursor-pointer"
		use:tooltip={{
			content: 'Create a new instance',
			position: 'bottom',
			background: '!bg-active-token',
			regionTooltip: 'text-sm',
			padding: 'px-2',
			width: 'max-w-max',
			color: 'text-slate-100'
		}}
		on:click={modal}
		on:keypress={modal}
	>
		<PackagePlus class="h-6 w-6 transition-colors duration-300 hover:text-[#f36]" />
	</div>
</div>

{#each data.devices as device (device.id)}
	<div transition:slide class="my-4 bg-white rounded-md shadow-md px-4 py-2">
		<div class="inline-block">
			<a
				href="devices/{device.id}"
				class="font-semibold cursor-pointer transition-colors duration-300 hover:decoration-2"
				>{device.name}
				<h2 class="font-sans font-normal text-xs inline text-slate-600">#{device.id}</h2></a
			>
			<p class="text-sm">{device.desc ? device.desc : 'No description'}</p>
		</div>
		<div class="float-right my-4 text-xs">
			Using definition: <span class="text-slate-600"
				>{device.definition && device.definition != 'NOT_AN_ITEM'
					? `#${device.definition}`
					: 'No definition'}</span
			>
		</div>
	</div>
{:else}
	<div>No devices have been instantiated yet!</div>
{/each}
