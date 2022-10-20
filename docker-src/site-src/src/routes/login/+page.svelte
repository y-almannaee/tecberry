<script lang="ts">
	import Dropdown from '$lib/dropdown.svelte';
	import { onMount } from 'svelte';

	let done = false,
		methods = [
			{
				id: 0,
				text: 'Use a sign-in token',
				link: 'https://google.com',
				primarycol: 'bg-slate-800',
				textcol: 'text-slate-50',
				hovercol: 'hover:bg-slate-800'
			},
			{
				id: 1,
				text: 'Sign-in with Google',
				link: 'https://google.com',
				primarycol: 'bg-blue-600',
				textcol: 'text-slate-50',
				hovercol: 'hover:bg-blue-500'
			}
		];
	onMount(() => {
		setTimeout(() => {
			done = true;
		}, 150);
	});
</script>

<div class="w-full flex items-center h-full bg-gray-50">
	<div
		class="bg-white dark:bg-slate-800 min-h-2/4 w-2/5 2xl:w-1/4 rounded p-8 shadow-xl mx-auto
		transition-all duration-700 {done ? '-translate-y-20 opacity-100' : 'translate-y-10 opacity-0'}"
	>
		<h1 class="font-semibold text-lg dark:text-slate-50">Choose a sign in method</h1>
		<span class="text-slate-400 italic text-sm w-3/5 block">
			These are specified by your organization, contact your IT if you are not able to log in
		</span>
		<div class="p-2 md:p-6 flex gap-4 flex-col items-center w-fit mx-auto">
			{#each methods as method (method.id)}
				<div on:click={()=>window.location=method.link}
					class="duration-300 cursor-pointer
				{method.hovercol} rounded py-2 px-4 text-center
				{method.primarycol} {method.textcol} w-full select-none
				hover:shadow-slate-900/20 hover:shadow-md transition-shadow"
				>
					{method.text}
				</div>
			{/each}
		</div>
	</div>
</div>
