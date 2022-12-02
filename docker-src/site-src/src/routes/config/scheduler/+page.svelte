<script>
	import { fade } from 'svelte/transition';
	import { AccordionGroup, AccordionItem, SlideToggle, tooltip } from '@skeletonlabs/skeleton';
	import { backend_url } from '$lib/global_objects';
	import { GripHorizontal } from 'lucide-svelte';
	import { Save } from 'lucide-svelte';
	import Sortable from '$lib/sortable.svelte';

	/** @type {import('./$types').PageData} */
	export let data;
	console.log(data);

	let config_type = false,
		validdata = false,
		disabled_arr = [],
		senddata = {},
		enabled_arr = (() => {
			if (data && data.scheduler.device_exec_order) {
				let enabled = data.scheduler.device_exec_order.split(',');
				let all_device_ids = [];
				data.devices.forEach((e) => {
					all_device_ids.push(e.id);
				});
				disabled_arr = all_device_ids.filter(function (el) {
					return enabled.indexOf(el) < 0;
				});
				return enabled;
			} else {
				let all_device_ids = [];
				data.devices.forEach((e) => {
					all_device_ids.push(e.id);
				});
				senddata.enabled = all_device_ids.join(',');
				return all_device_ids;
			}
		})(),
		dragging = false;

	senddata.on_start_code = data.scheduler.on_start_code || "";
	senddata.on_end_code = data.scheduler.on_end_code || "";

	// SIMPLE CONFIGURATION
	let total_duration = parseInt(data.scheduler.duration),
		amplitude = parseInt(data.scheduler.amplitude),
		offset = parseInt(data.scheduler.offset),
		period = parseInt(data.scheduler.period),
		phase_shift = parseInt(data.scheduler.phase_shift);
	import { Line } from 'svelte-chartjs';
	import { spring } from 'svelte/motion';

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
	let sinusoidal_data;
	let lineData,
		lineOptions = {
			responsive: true,
			animation: false,
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
				},
				tooltip: {
					displayColors: false,
					callbacks: {
						title: (ctx) => {
							return '';
						},
						label: (ctx) => {
							let label = '';
							if (ctx.parsed.y !== null && ctx.parsed.x !== null) {
								label = `${Math.round(ctx.parsed.y)}°C at ${Math.round(ctx.parsed.x)} mins`;
							}
							return label;
						}
					}
				}
			}
		};

	function generate_simple_data() {
		let arr = [];
		for (let i = 0; i < total_duration * 2; i++) {
			let x = i / 2;
			arr.push({
				x: x,
				y: offset + amplitude * Math.sin((Math.PI * 2 * (x + phase_shift)) / period)
			});
		}
		if (($sinusoidal_data && $sinusoidal_data.length !== arr.length) || !$sinusoidal_data) {
			sinusoidal_data = spring(arr);
			sinusoidal_data.damping = 0.6;
			sinusoidal_data.stiffness = 0.06;
		} else sinusoidal_data.set(arr);
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
			phase_shift != undefined &&
			period != 0
		) {
			generate_simple_data();
			validdata = true;
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
						data: $sinusoidal_data
					}
				]
			};
		} else {
			validdata = false;
		}
	}

	async function send_data() {
		let backend = backend_url(`/scheduler`);
		const res = await fetch(backend, { method: 'POST', body: JSON.stringify(senddata) });
	}

	$: {
		senddata.simple = !config_type;
		senddata.settings = {
			total_duration: total_duration,
			period: period,
			offset: offset,
			amplitude: amplitude,
			phase_shift: phase_shift
		};
	}
</script>

<div class="px-4 mt-12 md:mt-16 md:px-28">
	<h1 class="font-sans font-semibold inline mr-2">Scheduler</h1>
	<div
		class="inline-block align-text-bottom cursor-pointer"
		use:tooltip={{
			content: 'Save current settings',
			position: 'bottom',
			background: '!bg-active-token',
			regionTooltip: 'text-sm',
			padding: 'px-2',
			width: 'max-w-max',
			color: 'text-slate-100'
		}}
		on:click={send_data}
		on:keypress={send_data}
	>
		<Save
			class="h-6 w-6 transition-colors duration-300 {validdata
				? 'hover:text-[#f36]'
				: 'text-gray-300'}"
		/>
	</div>
	<!-- <div class="flex space-x-4 place-content-center my-4 bg-white rounded-md shadow-md px-4 py-2">
		<span class="mt-1">Simple</span>
		<SlideToggle
			bind:checked={config_type}
			label="Enable advanced scheduling"
			accent="bg-slate-300"
			class="bg-slate-300 shadow-md rounded-full"
		/>
		<span class="mt-1">Advanced</span>
	</div> -->
	<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
		<h2 class="font-sans font-semibold">
			<!-- {config_type ? 'Advanced configuration' : 'Simple configuration'} -->
			Settings
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
	<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
		<AccordionGroup>
			<AccordionItem>
				<svelte:fragment slot="summary">
					<div class="font-sans font-semibold">Start code</div>
					<div class="text-xs text-slate-700">
						This code executes when the scheduler starts running
					</div>
				</svelte:fragment>
				<svelte:fragment slot="content"
					><label>
						<textarea
							class="-mt-2 rounded-md -z-10 h-36 duration-75 overflow-hidden"
							class:font-mono={senddata.on_start_code}
							type="hidden"
							bind:value={senddata.on_start_code}
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
					</label></svelte:fragment
				>
			</AccordionItem>
			<AccordionItem>
				<svelte:fragment slot="summary">
					<div class="font-sans font-semibold">End code</div>
					<div class="text-xs text-slate-700">
						This code executes when the scheduler finishes running
					</div>
				</svelte:fragment>
				<svelte:fragment slot="content"
					><label transition:fade>
						<textarea
							class="-mt-2 rounded-md -z-10 h-36 duration-75 overflow-hidden"
							class:font-mono={senddata.on_end_code}
							type="hidden"
							bind:value={senddata.on_end_code}
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
					</label></svelte:fragment
				>
			</AccordionItem>
		</AccordionGroup>
	</div>
	<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">
		<h2 class="font-sans font-semibold">Device instance execution order</h2>
		<div class="text-xs text-slate-700">
			Devices near the top execute their code earlier than those towards the bottom. If a device
			instance relies on the value of another device then it should be placed after the device it
			relies on.
		</div>
		{#if (data.devices && data.devices.length == 0) || !data.devices}
			<div class="p-2 md:p-6 flex gap-4 flex-col items-center w-fit mx-auto">
				No devices created
			</div>
		{:else}
			<div class="text-sm px-4 mt-6 mb-36 gap-12 flex flex-row justify-center basis-2 grow">
				<div>
					<h1 class="font-sans mb-2">Enabled devices</h1>
					<div
						class="bg-white transition-colors duration-300 border-dashed border-2 {dragging
							? 'border-slate-600 bg-slate-200'
							: 'border-white bg-white'} rounded-md px-2 max-h-96 overflow-scroll min-w-[12rem] min-h-[24rem]"
					>
						<Sortable
							items={enabled_arr}
							options={{
								animation: 270,
								ghostClass: 'bg-slate-100',
								dragClass: 'opacity-0',
								group: 'devices',
								direction: 'vertical',
								onAdd: (e) => {
									e.item.classList.remove('!bg-gray-400', 'opacity-40');
									e.item.classList.add('shadow-md');
								},
								onStart: (e) => {
									dragging = true;
								},
								onEnd: (e) => {
									dragging = false;
								},
								store: {
									get: (arr) => {
										return enabled_arr;
									},
									set: (arr) => {
										let order = arr.toArray().join();
										senddata.enabled = order;
									}
								}
							}}
							let:item
							div_class="min-h-[12rem]"
						>
							<div
								data-id={item}
								class="cursor-grab shadow-md bg-white transition-colors duration-300 my-2 p-2 rounded-md"
							>
								<div class="inline-block">
									<h1 class="inline">{data.devices.find((e) => e.id == item).name}</h1>
									<h2 class="text-xs inline text-slate-600">#{item}</h2>
									<div class="text-xs text-slate-800">
										{data.devices.find((e) => e.id == item).desc
											? data.devices.find((e) => e.id == item).desc
											: 'No description'}
									</div>
								</div>
								<GripHorizontal class="h-8 mt-1 text-slate-600 inline float-right" />
							</div>
						</Sortable>
					</div>
				</div>
				<div>
					<h1 class="font-sans mb-2">Disabled devices</h1>
					<div
						class="bg-white transition-colors duration-300 border-dashed border-2 {dragging
							? 'border-slate-600 bg-slate-200'
							: 'border-white bg-white'} rounded-md px-2 max-h-96 overflow-scroll min-w-[12rem] min-h-[24rem]"
					>
						<Sortable
							items={disabled_arr}
							options={{
								animation: 270,
								ghostClass: 'bg-slate-100',
								dragClass: 'opacity-0',
								group: 'devices',
								direction: 'vertical',
								onAdd: (e) => {
									e.item.classList.add('!bg-gray-400', 'opacity-40');
									e.item.classList.remove('shadow-md');
								},
								onStart: (e) => {
									dragging = true;
								},
								onEnd: (e) => {
									dragging = false;
								},
								store: {
									get: (arr) => {
										return disabled_arr;
									},
									set: (arr) => {
										let order = arr.toArray().join();
										senddata.disabled = order;
									}
								}
							}}
							let:item
							div_class="min-h-[12rem]"
						>
							<div
								data-id={item}
								class="cursor-grab !bg-gray-400 opacity-40 bg-white transition-colors duration-300 my-2 p-2 rounded-md"
							>
								<div class="inline-block">
									<h1 class="inline">{data.devices.find((e) => e.id == item).name}</h1>
									<h2 class="text-xs inline text-slate-600">#{item}</h2>
									<div class="text-xs text-slate-800">
										{data.devices.find((e) => e.id == item).desc
											? data.devices.find((e) => e.id == item).desc
											: 'No description'}
									</div>
								</div>
								<GripHorizontal class="h-8 mt-1 text-slate-600 inline float-right" />
							</div>
						</Sortable>
					</div>
				</div>
			</div>
		{/if}
	</div>
</div>
