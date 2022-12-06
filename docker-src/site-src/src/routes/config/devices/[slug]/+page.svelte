<script>
	/** @type {import('./$types').PageData} */
	export let data;
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { expoIn } from 'svelte/easing';
	import { Save, Trash2 } from 'lucide-svelte';
	import { tooltip, Modal, modalStore, ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
	import { backend_url } from '$lib/global_objects';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { writable } from 'svelte/store';

	let ready = false;
	onMount(() => {
		ready = true;
	});

	function modal() {
		const confirm = {
			type: 'confirm',
			title: 'Confirm deletion',
			body: `Are you sure you wish to delete ${data.self.name}?`,
			// confirm = TRUE | cancel = FALSE
			response: async (r) => {
				if (r == true) {
					let backend = backend_url(`/devices/${data.self.id}`);
					const res = await fetch(backend, { method: 'DELETE' });
					goto('/config/devices');
				}
			}
		};
		modalStore.trigger(confirm);
	}

	async function save_dev() {
		let backend = backend_url( `/devices/${data.self.id}`);
		let mutableData = structuredClone(data.self);
		delete mutableData.id;
		delete mutableData.name;
		const res = await fetch(backend, { method: 'POST', body: JSON.stringify(mutableData) });
		goto('/config/devices');
	}

	let current_def_sel = writable(data.self.definition ? data.self.definition : 'NOT_AN_ITEM'), current_def=null;
	$: {
		if ($current_def_sel && $current_def_sel!="NOT_AN_ITEM") {
			data.self.definition = $current_def_sel
			current_def = data.definitions.find((v, i) => v.id == $current_def_sel);
			if (current_def && current_def.public) {
				current_def.public.split(',').some((e) => {
					if (!data.self.public) {
						data.self.public = {};
						for (const key of current_def.public.split(',')) {
							data.self.public[key] = '';
						}
						return true;
					}
					if (data.self.public && !data.self.public[e]) {
						data.self.public[e] = '';
					}
				});
			}
			if (current_def && current_def.private) {
				current_def.private.split(',').some((e) => {
					if (!data.self.private) {
						data.self.private = {};
						for (const key of current_def.private.split(',')) {
							data.self.private[key] = '';
						}
						return true;
					}
					if (data.self.private && !data.self.private[e]) {
						data.self.private[e] = '';
					}
				});
			}
		} else {
			data.self.definition = $current_def_sel
			current_def = '';
		}
	}

	$: console.log($current_def_sel)
</script>

<svelte:head> 
	<title>Viewing device {data.self.name}#{data.self.id} | TECBERRY.ml</title>
</svelte:head>

<Modal regionBackdrop="bg-backdrop-token backdrop-blur-sm" />
{#if ready}
	<div in:fly={{ duration: 300, y: 200, opacity: 0, easing: expoIn }}>
		<h1 class="font-sans font-semibold inline">{data.self.name}</h1>
		<h2 class="font-sans text-xs inline text-slate-600">#{data.self.id}</h2>
		<div class="mb-2 outline-offset-2" contenteditable bind:textContent={data.self.desc}>
			{data.self.desc ? data.self.desc : 'No description'}
		</div>
		<div
			class="inline-block cursor-pointer"
			use:tooltip={{
				content: 'Save this instance',
				position: 'bottom',
			background: '!bg-active-token',regionTooltip: 'text-sm',
				padding: 'px-2',
				width: 'max-w-max',
				color: 'text-slate-100'
			}}
			on:click={save_dev}
			on:keypress={save_dev}
		>
			<Save class="h-6 w-6 transition-colors duration-300 hover:text-[#f36]" />
		</div>
		<div
			class="inline-block cursor-pointer"
			use:tooltip={{
				content: 'Delete this instance',
				position: 'bottom',
			background: '!bg-active-token',regionTooltip: 'text-sm',
				padding: 'px-2',
				width: 'max-w-max',
				color: 'text-slate-100'
			}}
			on:click={modal}
			on:keypress={modal}
		>
			<Trash2 class="h-6 w-6 transition-colors duration-300 hover:text-[#f36]" />
		</div>
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
			<ListBox selected="{current_def_sel}" accent="!bg-active-token !text-slate-50" label="Definition">
				<ListBoxItem value={'NOT_AN_ITEM'}>No definition</ListBoxItem>
				{#each data.definitions as def}
					<ListBoxItem value={def.id}>
						{def.name}#{def.id}
					</ListBoxItem>
				{/each}
			</ListBox>
			<!-- <select class="rounded-md w-36 m-2" bind:value={data.self.definition}>
				<option value={null}>
					No definition
				</option>
				{#each data.definitions as def}
					<option value={def.id}>
						{def.name}#{def.id}
					</option>
				{/each}
			</select> -->
		</div>
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
			<div>
				<div class="font-sans font-semibold">Public variables</div>
				<div class="text-xs text-slate-700">
					These variables are accessible by other device instances
				</div>
				{#if current_def && current_def.public}
					{#each current_def.public.split(',') as public_var}
						<label class="font-mono my-2"
							>{public_var} =
							<input
								class="rounded-md font-mono px-2 py-1 w-36"
								type="text"
								bind:value={data.self.public[public_var]}
							/></label
						>
					{/each}
				{:else if current_def && !current_def.public}
					<div>No public variables have been declared by this definition</div>
				{:else}
					<div>Please specify a definition</div>
				{/if}
			</div>
		</div>
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
			<div>
				<div class="font-sans font-semibold">Private variables</div>
				<div class="text-xs text-slate-700">
					These variables are only accessible by this device instance
				</div>
				{#if current_def && current_def.private}
					{#each current_def.private.split(',') as private_var}
						<label class="font-mono my-2"
							>{private_var} =
							<input
								class="rounded-md font-mono px-2 py-1 w-36"
								type="text"
								bind:value={data.self.private[private_var]}
							/></label
						>
					{/each}
				{:else if current_def && !current_def.private}
					<div>No private variables have been declared by this definition</div>
				{:else}
					<div>Please specify a definition</div>
				{/if}
			</div>
		</div>
	</div>
{/if}
