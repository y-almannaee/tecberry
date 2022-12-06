<script>
	import { asyncReadable } from '@square/svelte-store';
	import { backend_url } from '$lib/global_objects';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { VideoOff } from 'lucide-svelte';
	import { browser, dev } from '$app/environment';
	import videojs from 'video.js';
	import { onMount } from 'svelte';
	import { onDestroy } from 'svelte';

	// SIMPLE CONFIGURATION
	let total_duration, amplitude, offset, period, phase_shift;
	import { Line } from 'svelte-chartjs';
	import { spring } from 'svelte/motion';

	import {
		Chart as ChartJS,
		Title,
		Tooltip,
		Legend,
		LineElement,
		LinearScale,
		PointElement
	} from 'chart.js';

	ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement);
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
					display: false,
					labels: {
						usePointStyle: true,
					}
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
								label = `${ctx.dataset.label=="You are here"? "Currently at ":""}${Math.round(ctx.parsed.y)}°C at ${Math.round(ctx.parsed.x)} mins`;
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

	let video_element,
		video_go_ahead = false,
		videojs_reference,
		videojs_error = false,
		checker_timeout,
		videojs_options = {
			autoplay: 'any',
			controls: true,
			poster: '/stream_waiting.png',
			preload: 'auto',
			liveui: true,
			// fluid: true,
			responsive: true
		};

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

	const folder_dash = 'https://demo.tecberry.ml/stream/dash/';
	const video_tracks_dash = asyncReadable(
		{},
		async () => {
			try {
				const res = await fetch(folder_dash);
				if (res && res.ok) {
					let info_data = await res.json();
					let cut_data = info_data.flatMap((e) => {
						if (e.name && e.name.endsWith('.mpd')) return `${folder_dash}${e.name}`;
						else return [];
					});
					return cut_data;
				}
			} catch (e) {
				return [];
			}
		},
		{ reloadable: true }
	);

	const folder_hls = 'https://demo.tecberry.ml/stream/hls/';
	const video_tracks_hls = asyncReadable(
		{},
		async () => {
			try {
				const res = await fetch(folder_hls);
				if (res && res.ok) {
					let info_data = await res.json();
					let cut_data = info_data.flatMap((e) => {
						if (e.name && e.name.endsWith('.m3u8')) return `${folder_hls}${e.name}`;
						else return [];
					});
					return cut_data;
				}
			} catch (e) {
				return [];
			}
		},
		{ reloadable: true }
	);

	onMount(() => {
		if (browser) {
			video_go_ahead = true;
		}
		const a = () => {
			if (info) info.reload();
			if (video_tracks_hls) video_tracks_hls.reload();
			if (video_tracks_dash) video_tracks_dash.reload();
			checker_timeout = setTimeout(a, 1000);
		};
		checker_timeout = setTimeout(a, 1000);
	});

	onDestroy(() => {
		if (browser && videojs_reference) {
			videojs_reference.dispose();
		}
		clearTimeout(checker_timeout);
	});

	$: if (video_element && video_go_ahead) {
		videojs_reference = videojs(video_element, videojs_options);
		videojs_reference.on('ended', () => {
			videojs_reference.hasStarted(false);
		});
		videojs_reference.on('error', () => {
			videojs_reference.dispose();
			videojs_error = true;
		});
	}
	$: {
		if ($info && $info.running && $info.running.settings) {
			total_duration = $info.running.settings.duration;
			offset = $info.running.settings.offset;
			phase_shift = $info.running.settings.phase_shift;
			amplitude = $info.running.settings.amplitude;
			period = $info.running.settings.period;
			generate_simple_data();
			if($info.running.running){
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
						},
						{
							label: 'You are here',
							fill: false,
							backgroundColor: 'rgba(225, 204,230, .3)',
							borderColor: 'rgb(185, 28, 28)',
							borderWidth: 1,
							pointStyle: 'circle',
							pointRadius: 3,
							pointBorderColor: 'rgb(185, 28, 28)',
							data: [$sinusoidal_data[Math.round(2*$info.running.time_elapsed/60)]]
						}
					]
				};}
			else
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
		}
	}
</script>

<svelte:head>
	{#if $info.running && $info.running.running && $info.running.settings && $info.running.settings.duration}
		{@const tl = Math.floor($info.running.settings.duration - $info.running.time_elapsed / 60)}
		<title>Insight: {tl} {tl != 1 ? 'minutes' : 'minute'} left | TECBERRY.ml</title>
	{:else}
		<title>Insight | TECBERRY.ml</title>
	{/if}
</svelte:head>

{#await info.load()}
	<div class="w-full h-full justify-center items-center flex">
		<div class="max-w-[4rem] max-h-[4rem] w-full">
			<ProgressRadial stroke={150} meter="stroke-primary-500" fill="fill-accent" />
		</div>
	</div>
{:then}
	<div class="mt-16 m-4">
		<div class="flex gap-4 mb-4">
			<div class="w-70 bg-white rounded-md shadow-md p-6">
				{#if !videojs_error && $video_tracks_dash.length && $video_tracks_hls.length}
					<!-- svelte-ignore a11y-media-has-caption -->
					<video-js
						bind:this={video_element}
						class="video-js w-64 md:w-96 lg:w-[38rem] aspect-[4/3]"
					>
						{#each $video_tracks_dash as track}
							<source src={track} type="application/dash+xml" />
						{:else}
							<!--Nothing-->
						{/each}
						{#each $video_tracks_hls as track}
							<source src={track} type="application/x-mpegURL" />
						{:else}
							<!--Nothing-->
						{/each}
					</video-js>
				{:else}
					<div class="w-full justify-center flex flex-col">
						<div>
							<VideoOff class="w-28 h-28 text-slate-700 m-auto" />
						</div>
						<div class="mt-2">An error has occurred with live playback</div>
					</div>
				{/if}
			</div>
			<div class="bg-white rounded-md grow justify-center items-center flex shadow-md p-6">
				<button
					class="bg-green-600 shadow-md hover:scale-110 duration-300 will-change-transform hover:bg-green-500 rounded-md w-16 h-16 text-white"
					on:click={async () => {
						let start_url = backend_url('/monitor');
						let res = await fetch(start_url, { method: 'POST' });
						if (res.ok && info) {
							info.reload();
						}
					}}
				>
					Start
				</button>
				<button
					class="bg-red-700 ml-4 shadow-md hover:scale-110 duration-300 will-change-transform hover:bg--red-600 rounded-md w-16 h-16 text-white"
					on:click={async () => {
						let start_url = backend_url('/monitor');
						let res = await fetch(start_url, { method: 'DELETE' });
						if (res.ok && info) {
							info.reload();
						}
					}}
				>
					Stop
				</button>
			</div>
			<div class="bg-white rounded-md shadow-md p-6 w-fit">
				<div class="max-w-sm">
					<Line data={lineData} options={lineOptions} />
				</div>
			</div>
		</div>
		{#if $info.running.running}
			<div class="w-full grid grid-col grid-cols-4 gap-4">
				{#each Object.entries($info.running.devices) as [id, device]}
					<div class="bg-white rounded-md aspect-square w-38 h-38 shadow-md px-4 py-2">
						<h1 class="font-sans font-semibold inline">{device.name}</h1>
						<h2 class="font-sans text-xs inline text-slate-600">#{id}</h2>
						<div>
							{#each Object.entries(device.public) as [key, value]}
								<div class="last:border-b last:rounded">{key}= {value}</div>
							{:else}
								<!--Nothing-->
							{/each}
						</div>
						<div>
							{#each Object.entries(device.private) as [key, value]}
								<div class="text-slate-600 first:mt-2 text-sm">{key}= {value}</div>
							{:else}
								<!--Nothing-->
							{/each}
						</div>
					</div>
				{/each}
			</div>
		{:else}{/if}
		{#if dev}
			<div class="my-4 bg-white rounded-md shadow-md px-4 py-2">{JSON.stringify($info)}</div>
		{/if}
	</div>
{/await}

<style global>
	@import '$lib/video-js.min';
</style>
