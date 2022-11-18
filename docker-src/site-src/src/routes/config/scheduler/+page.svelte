<script>
	import { SlideToggle, tooltip } from '@brainandbones/skeleton';
	/** @type {import('./$types').PageData} */
	export let data;

	let config_type = false;

	// SIMPLE CONFIGURATION
	let total_duration = 300,
		amplitude = 55,
		offset = 25,
		period = 150,
		phase_shift = 0;
	import { Line } from 'svelte-chartjs';

	import {
		Chart as ChartJS,
		Title,
		Tooltip,
		Legend,
		LineElement,
		LinearScale,
		PointElement,
		CategoryScale
	} from 'chart.js';

	ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale);
	let lineData,
		lineOptions = {
			responsive: true,
			maintainAspectRatio: false,
			scales: {
				x: {
					title: { display: true, text: 'Time (mins)' },
					display: true,
					type: 'linear',
					grid: {
						display: false
					}
				},
				y: {
					title: { display: true, text: 'Temperature (°C)' },
					grid: {
						display: false
					}
				}
			},
			plugins: {
				legend: {
					display: false
				}
			}
		};

	function generate_simple_data(total_duration, period, amplitude, offset) {
		let arr = [];
		for (let i = 0; i < total_duration * 2; i++) {
			let x = i / 2;
			arr.push({ x: x, y: offset + amplitude * Math.sin((Math.PI * (x + phase_shift)) / period) });
		}
		return arr;
	}

	$: {
		if (
			total_duration != NaN &&
			period != NaN &&
			amplitude != NaN &&
			offset != NaN &&
			phase_shift != NaN &&
			total_duration != undefined &&
			period != undefined &&
			amplitude != undefined &&
			offset != undefined &&
			phase_shift != undefined
		) {
			lineData = {
				datasets: [
					{
						label: 'Simple configuration',
						fill: true,
						lineTension: 0.3,
						backgroundColor: 'rgba(225, 204,230, .3)',
						borderColor: 'rgb(185, 28, 28)',
						borderCapStyle: 'round',
						borderDash: [],
						borderDashOffset: 0.0,
						borderJoinStyle: 'miter',
						pointRadius: 0,
						data: generate_simple_data(total_duration, period, amplitude, offset)
					}
				]
			};
		}
	}
</script>

<div class="p-4 md:px-28">
	<h1 class="font-semibold font-sans">Scheduler</h1>
	<div class="flex space-x-4 place-content-center my-4 bg-white rounded-md shadow-md px-4 py-2">
		<span class="mt-1">Simple</span>
		<SlideToggle
			bind:checked={config_type}
			label="Enable advanced scheduling"
			accent="bg-slate-300"
			class="bg-slate-300 shadow-md rounded-full"
		/>
		<span class="mt-1">Advanced</span>
	</div>
	<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
		<h2 href="devices/" class="font-sans font-semibold">
			{config_type ? 'Advanced configuration' : 'Simple configuration'}
		</h2>
		<div class="text-sm grid grid-cols-2 gap-6">
			{#if config_type}
				<p>advanced</p>
			{:else}
				<div class="w-40 lg:w-80 grid grid-cols-2 lg:grid-cols-3 gap-4">
					<div>
						Duration <input class="rounded-md p-1" type="number" bind:value={total_duration} />
					</div>
					<div>Period <input class="rounded-md p-1" type="number" bind:value={period} /></div>
					<div>Amplitude <input class="rounded-md p-1" type="number" bind:value={amplitude} /></div>
					<div>Offset <input class="rounded-md p-1" type="number" bind:value={offset} /></div>
					<div>
						Phase Shift <input class="rounded-md p-1" type="number" bind:value={phase_shift} />
					</div>
				</div>
				<div class="max-w-sm">
					<Line data={lineData} options={lineOptions} />
				</div>
			{/if}
		</div>
	</div>
</div>
