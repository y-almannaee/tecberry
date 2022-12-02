<script>
	import { asyncReadable } from '@square/svelte-store';
	import { backend_url } from '$lib/global_objects';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	const info = asyncReadable(
		{},
		async () => {
			let backend_info = backend_url('/monitor');
			let info_ok = false;
			while (!info_ok) {
				try {
					const res = await fetch(backend_info);
					if (res && res.ok) {
						let info_data = await res.json();
						info_ok = true;
						return info_data;
					}
				} catch (e) {
					info_ok = false;
					await new Promise((r, e) => setTimeout(r, 1500));
				}
			}
		},
		{ reloadable: true }
	);

	$: console.log($info)
</script>

{#await info.load()}
	<div class="w-full h-full justify-center items-center flex">
		<div class="max-w-[4rem] max-h-[4rem] w-full">
			<ProgressRadial stroke={150} meter="stroke-primary-500" fill="fill-accent" />
		</div>
	</div>
{:then}
	<div class="mt-16 m-4">
		<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">{JSON.stringify($info)}</div>
	</div>
{/await}
