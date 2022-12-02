<script>
	import { slide } from 'svelte/transition';
	import { FilePlus } from 'lucide-svelte';
	import { Modal, tooltip, modalStore } from '@skeletonlabs/skeleton';
	import { backend_url } from '$lib/global_objects';
	import { invalidate } from '$app/navigation';

	let anim = true;
	export let data;
	function modal() {
		const confirm = {
			type: 'prompt',
			title: 'Enter definition name',
			body: 'Please provide a recognizable name for your definition',
			// confirm = TRUE | cancel = FALSE
			response: async (r) => {
				if (r == false) return;
				let backend = backend_url('/definitions');
				const res = await fetch(backend, { method: 'POST', body: JSON.stringify({ name: r }) });
				invalidate((url) => true);
			}
		};
		modalStore.trigger(confirm);
	}
</script>

<Modal
	regionBackdrop="bg-backdrop-token backdrop-blur-sm"
	on:keydown={(e) => {
		if (e.key == 'Enter') document.querySelector('.btn-filled-primary').click();
	}}
/>

<div>
	<h1 class="font-sans font-semibold">List of device definitions</h1>
	<div>The following definitions exist</div>
	<div
		class="inline-block cursor-pointer"
		use:tooltip={{
			content: 'Create a new definition',
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
		<FilePlus class="h-6 w-6 transition-colors duration-300 hover:text-[#f36]" />
	</div>
</div>

{#each data.definitions as definition (definition.id)}
	<div transition:slide class="my-4 bg-white rounded-md shadow-md px-4 py-2">
		<a
			href="definitions/{definition.id}"
			class="font-semibold cursor-pointer transition-colors duration-300 hover:decoration-2"
			>{definition.name}
			<h2 class="font-sans font-normal text-xs inline text-slate-600">#{definition.id}</h2></a
		>
		<p class="text-sm">{definition.desc ? definition.desc : 'No description'}</p>
	</div>
{/each}
