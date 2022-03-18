<script>
	import { onMount } from 'svelte';
	import Line from 'svelte-chartjs/src/Line.svelte';

	let directives = [
			{ id: 0, directive: 'rise', duration: 300, to: 40 },
			{ id: 1, directive: 'dwell', duration: 300 },
			{ id: 2, directive: 'return', duration: 300, to: 37 }
		],
		feeds = [
			{ id: 0, text: `No video device` },
			{ id: 1, text: `Generic Webcam` },
			{ id: 2, text: `Thermal Camera MLX90641` }
		];

	let feed_selected,
		t = 0,
		temp_ambient = 25.5,
		temp_tmp36_1 = 36.5,
		read_as_sensor = true;
	setInterval(() => {
		temp_tmp36_1 =
			37 + Math.round((Math.sin((t++ * Math.PI) / 180) + Number.EPSILON) * 10) / 10 - 0.5;
		temp_ambient =
			26 + Math.round((Math.sin((t++ * Math.PI) / 180) + Number.EPSILON) * 10) / 10 - 0.5;
		t %= 360;
	}, 3500);

	let action_id,
		action_directive,
		action_seconds,
		action_to,
		start_from = 24;

	onMount(() => {
		create_data();
		setTimeout(create_data, 3000);
	});

	const down = (ctx, value) => (ctx.p0.parsed.y > ctx.p1.parsed.y ? value : undefined);

	let dataline = {
		datasets: [
			{
				label: '',
				fill: false,
				lineTension: 0.25,
				backgroundColor: '#ff3366',
				borderColor: '#ff3366',
				borderCapStyle: 'butt',
				borderDash: [],
				borderDashOffset: 0.0,
				borderJoinStyle: 'miter',
				pointHoverRadius: 5,
				pointHoverBackgroundColor: 'rgb(0, 0, 0)',
				pointHoverBorderColor: 'rgba(220, 220, 220,1)',
				pointHoverBorderWidth: 2,
				pointRadius: 1,
				pointHitRadius: 10,
				segment: {
					borderColor: (ctx) => down(ctx, '#4D6CFA')
				},
				data: [
					{ x: 0, y: 24 },
					{ x: 300, y: 40 },
					{ x: 600, y: 40 },
					{ x: 900, y: 37 }
				]
			}
		]
	};

	let options = {
		scales: {
			xAxis: {
				type: 'linear',
				title: {
					display: true,
					text: 'Time (s)'
				}
			},
			yAxis: {
				title: {
					display: true,
					text: 'Temperature (°C)'
				}
			}
		},
		plugins: {
			legend: {
				position: 'bottom',
				display: false
			}
		}
	};

	function create_data() {
		let x = 0;
		let y = start_from;
		dataline.datasets[0].data = [{ x: x, y: y }];
		for (let i = 0; i < directives.length; i++) {
			let final_y;
			if (directives[i].directive == 'dwell') {
				final_y = directives[i - 1].to || start_from;
			} else {
				final_y = directives[i].to;
			}
			x += directives[i].duration;
			y = final_y;
			let point = { x: x, y: y };
			dataline.datasets[0].data.push(point);
		}
		let point = {
			x:
				dataline.datasets[0].data[dataline.datasets[0].data.length - 1].x +
				10 *
					Math.abs(dataline.datasets[0].data[dataline.datasets[0].data.length - 1].y - start_from),
			y: start_from
		};
		dataline.datasets[0].data.push(point);
		dataline = dataline;
		console.log(dataline);
	}

	function add_action() {
		console.log(action_directive);
		console.log(action_id);
		console.log(action_seconds);
		console.log(action_to);
		directives.push({
			id: action_id,
			directive: action_directive,
			duration: action_seconds,
			to: action_to
		});
		directives = directives;
		create_data();
	}
</script>

<div class="row">
	<div class="column">
		<div class="row">
			<div class="column" style="max-width: 45%">
				<span class="controls"
					><h3>Temperatures</h3>
					<p>Ambient: {temp_ambient}°C</p>
					<p>TMP36-1: {temp_tmp36_1}°C</p>
					{#if read_as_sensor}
						<p>MLX90641: 37.2°C</p>
					{/if}
				</span>
			</div>
			<div class="column">
				<span class="controls">
					<h3>Active GPIO Devices</h3>
					<p>Peltier-1: heating&emsp;Peltier-2: heating</p>
					<p>Peltier-3: heating&emsp;Peltier-4: heating</p>
					<p>Peltier-5: heating&emsp;Peltier-6: heating</p>
				</span>
			</div>
		</div>

		<span class="controls">
			<select bind:value={feed_selected} style="float: right; margin: 4px 0;">
				{#each feeds as feed}
					<option value={feed.id}>
						{feed.text}
					</option>
				{/each}
			</select>
			<h3>Video</h3>
			{#if feed_selected == 1}
				<img src="/images/video_example.jpg" alt="Video feed example" width="100%" />
			{:else if feed_selected == 2}
				<img src="/images/thermal_example.jpg" alt="Thermal feed example" width="100%" />
				<label
					><input type="checkbox" bind:checked={read_as_sensor} />Read temperature as sensor</label
				>
			{:else}
				<p>No video selected</p>
			{/if}
		</span>
	</div>
	<div class="column">
		<span class="controls"
			><h3>Configured Curve</h3>
			<Line data={dataline} {options} /></span
		>
		<span class="controls">
			<div class="options" />
			<h3>Curve configuration</h3>
			{#each directives as directive (directive.id)}
				<p>
					Action {directive.id}:
					<select bind:value={directive.directive}
						><option>rise</option><option>dwell</option><option>return</option></select
					>
					for
					<input bind:value={directive.duration} on:blur={create_data} type="number" /> seconds
					{#if directive.directive == 'rise' || directive.directive == 'return'}
						to <input bind:value={directive.to} on:blur={create_data} type="number" /> °C
					{/if}
				</p>
			{/each}
			<p>
				New action <input type="number" bind:value={action_id} />:
				<select bind:value={action_directive}
					><option>rise</option><option>dwell</option><option>return</option></select
				>
				for <input type="number" bind:value={action_seconds} /> seconds
				{#if action_directive == 'rise' || action_directive == 'return'}
					to <input bind:value={action_to} type="number" /> °C
				{/if}
				<button on:click={add_action}>Add</button>
			</p>
			<label
				>Start from <input type="number" bind:value={start_from} on:blur={create_data} />°C</label
			>
		</span>
	</div>
	<div class="column">
		<span class="controls"
			><h3>Statistics</h3>
			Time left
		</span>
	</div>
</div>
<p style="font-size: smaller; opacity: 0.7;">
	Not feature complete, not indicative of final design
</p>

<style>
	.row {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		padding: 0 4px;
	}
	.column {
		flex: 50%;
		max-width: 50%;
	}

	.controls {
		display: block;
		padding: 4px;
		border-radius: 12px;
		min-height: 4em;
		width: 90%;
		margin: 5px;
		-webkit-box-shadow: 0px 0px 12px -2px rgba(1, 22, 39, 0.22);
		-moz-box-shadow: 0px 0px 12px -2px rgba(1, 22, 39, 0.22);
		box-shadow: 0px 0px 12px -2px rgba(1, 22, 39, 0.22);
	}

	.options {
		width: 1em;
		height: 1em;
		border-radius: 30px;
		background-image: radial-gradient(circle, #01162744 1px, transparent 2px);
		transition: box-shadow 0.2s ease-in;
		background-size: 100% 33.33%;
		float: right;
		cursor: pointer;
		-webkit-box-shadow: 0px 0px 0px 0px rgba(0, 0, 0, 0.2);
		-moz-box-shadow: 0px 0px 0px 0px rgba(0, 0, 0, 0.2);
		box-shadow: 0px 0px 0px 0px rgba(0, 0, 0, 0.2);
	}

	.options:hover {
		-webkit-box-shadow: 0px 0px 4px 0px rgba(0, 0, 0, 0.2);
		-moz-box-shadow: 0px 0px 4px 0px rgba(0, 0, 0, 0.2);
		box-shadow: 0px 0px 4px 0px rgba(0, 0, 0, 0.2);
	}

	@media screen and (max-width: 800px) {
		.column {
			flex: 50%;
			max-width: 50%;
		}
	}

	@media screen and (max-width: 600px) {
		.column {
			flex: 100%;
			max-width: 100%;
		}
	}

	h3 {
		margin: 4px 0;
		color: var(--accent);
	}

	p {
		line-height: 0.5;
	}

	input::-webkit-inner-spin-button,
	input::-webkit-outer-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	input[type='number'] {
		width: 30px;
		appearance: none;
		-moz-appearance: textfield;
	}
</style>
