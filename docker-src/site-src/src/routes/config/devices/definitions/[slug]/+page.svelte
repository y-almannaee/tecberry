<script>
	/** @type {import('./$types').PageData} */
	export let data;
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { expoIn } from 'svelte/easing';
	import { Save, Trash2 } from 'lucide-svelte';
	import { tooltip, Modal, modalStore } from '@skeletonlabs/skeleton';
	import { backend_url } from '$lib/global_objects';
	import { goto } from '$app/navigation';

	let ready = false;
	onMount(() => (ready = true));

	function modal() {
		const confirm = {
			type: 'confirm',
			title: 'Confirm deletion',
			body: `Are you sure you wish to delete ${data.name}?`,
			response: async (r) => {
				if (r == true) {
					let backend = backend_url(`/definitions/${data.id}`);
					const res = await fetch(backend, { method: 'DELETE' });
					goto('/config/devices/definitions');
				}
			}
		};
		modalStore.trigger(confirm);
	}
	async function save_def() {
		let backend = backend_url(`/definitions/${data.id}`);
		let mutableData = structuredClone(data);
		delete mutableData.id;
		delete mutableData.name;
		const res = await fetch(backend, { method: 'POST', body: JSON.stringify(mutableData) });
		goto('/config/devices/definitions');
	}
</script>

<Modal regionBackdrop="bg-backdrop-token backdrop-blur-sm" />
{#if ready}
	<div in:fly={{ duration: 300, y: 200, opacity: 0, easing: expoIn }}>
		<div>
			<h1 class="font-sans font-semibold inline">{data.name}</h1>

			<h2 class="font-sans text-xs inline text-slate-600">#{data.id}</h2>
		</div>
		<div class="mb-2 outline-offset-2" contenteditable bind:textContent={data.desc}>
			{data.desc ? data.desc : 'No description'}
		</div>
		<div
			class="inline-block cursor-pointer"
			use:tooltip={{
				content: 'Save this definition',
				position: 'bottom',
			background: '!bg-active-token',regionTooltip: 'text-sm',
				padding: 'px-2',
				width: 'max-w-max',
				color: 'text-slate-100'
			}}
			on:click={save_def}
			on:keypress={save_def}
		>
			<Save class="h-6 w-6 transition-colors duration-300 hover:text-[#f36]" />
		</div>
		<div
			class="inline-block cursor-pointer"
			use:tooltip={{
				content: 'Delete this definition',
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
			<label>
				<div class="font-sans font-semibold">List of public variables</div>
				<div class="text-xs text-slate-700">
					These variables will be accessible by other instances, takes a comma-separated list of
					variables to expose
				</div>
				<input
					class="mt-2 rounded-md"
					placeholder="For example: x,y,temperature,humidity"
					type="text"
					bind:value={data.public}
				/>
			</label>
		</div>
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
			<label>
				<div class="font-sans font-semibold">List of private variables</div>
				<div class="text-xs text-slate-700">
					These variables will be assigned by someone who is instantiating this definition, but they
					won't be accessible by other instances, takes a comma-separated list of variables to
					expose
				</div>
				<input
					class="mt-2 rounded-md"
					placeholder="For example: pin_data,address,secret_value"
					type="text"
					bind:value={data.private}
				/>
			</label>
		</div>
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2 will-change-transform mb-72">
			<label>
				<div class="font-sans font-semibold">Code</div>
				<div class="text-xs text-slate-700">
					This code executes every time the scheduler prompts this device
				</div>
				<textarea
					class="mt-2 rounded-md -z-10 h-36 duration-75 overflow-hidden"
					class:font-mono={data.code}
					type="hidden"
					bind:value={data.code}
					on:keyup={(e) => {
						e.target.style.height =
							e.target.scrollHeight > e.target.clientHeight
								? e.target.scrollHeight + 'px'
								: '144px';
					}}
					on:keydown={(e) => {
						if (e.key != 'Tab') {
							return;
						}
						e.preventDefault();
						var start = e.target.selectionStart;
						var end = e.target.selectionEnd;

						// set textarea value to: text before caret + tab + text after caret
						e.target.value =
							e.target.value.substring(0, start) + '\t' + e.target.value.substring(end);

						// put caret at right position again
						e.target.selectionStart = e.target.selectionEnd = start + 1;
					}}
					placeholder="Type your code here..."
				/>
			</label>
		</div>
	</div>
{/if}
