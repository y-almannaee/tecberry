<script>
	import { Paginator } from '@skeletonlabs/skeleton';
	export let data;

	let page = {
			offset: 0,
			limit: 5,
			size: data.logs.length,
			amounts: [1, 2, 5, 10]
		},
		sourcePaginated;

	$: sourcePaginated = data.logs.slice(
		page.offset * page.limit, // start
		page.offset * page.limit + page.limit // end
	);

	const border_color_h = 'border-slate-100';
	const border_color_d = 'border-slate-200';
</script>

<div class="m-8 mt-16">
	<table class="text-xs p-1 border-spacing-y-1 border-spacing-x-4 bg-white shadow-md">
		<thead
			><tr
				><th class="">Time</th><th class="">Source</th
				><th class="">Log</th></tr
			></thead
		>
		<tbody>
			{#each sourcePaginated as row}
				<tr>
					<td class="">{row.split(';|#|')[0]}</td>
					<td
						class="text-ellipsis overflow-hidden max-w-[2rem]"
						title={row.split(';|#|')[1]}>{row.split(';|#|')[1]}</td>
					<td class="whitespace-pre max-w-lg overflow-hidden text-ellipsis">{row.split(';|#|')[2]}</td>
				</tr>
			{/each}
		</tbody>
	</table>
	<Paginator bind:settings={page} select={'rounded-md px-5 py-1'} />
</div>

<style>
	thead:first-child tr:first-child th:first-child,
	tbody:first-child tr:first-child td:first-child {
		border-radius: 0.5rem 0 0 0;
	}

	thead:last-child tr:last-child th:first-child,
	tbody:last-child tr:last-child td:first-child {
		border-radius: 0 0 0 0.5rem;
	}

	table {
		border-collapse: separate;
		border-left: 0;
		border-radius: 0.5rem;
	}
</style>
