<script>
	import { Stepper, Step } from '@brainandbones/skeleton';
	import { writable } from 'svelte/store';
	const active = writable(0);
	function onComplete() {
		return 1;
	}
</script>

<div class="my-8 mx-24">
	<Stepper
		{active}
		length={2}
		on:complete={onComplete}
		buttonNext="bg-slate-300 rounded-md text-sm px-2 py-1 mt-2 -mb-6"
		buttonBack="bg-slate-300 rounded-md text-sm px-2 py-1 mt-2 -mb-6"
		buttonComplete="bg-rose-400 rounded-md text-sm px-2 py-1 mt-2 -mb-6"
		background="bg-slate-900"
	>
		<Step index={0}>
			<h1 class="font-sans font-semibold" slot="header">
				Verify some basic facts about your TECBERRY
			</h1>
			hello
		</Step>
		<Step index={1} locked={true}>hello</Step>
	</Stepper>
</div>
