<script lang="ts">
	import { onMount } from 'svelte';
	import { tweened } from 'svelte/motion';
	import { expoOut } from 'svelte/easing';

	import Slide from '$lib/Slide.svelte';
	import Demo from '$lib/Demo.svelte';
	import Logo from '$lib/Logo.svelte';
	import TecModule from '$lib/TecModule.svelte';

	import PageNumber from '$lib/PageNumber.svelte';
	import ScrollToSlide from '$lib/ScrollToSlide.svelte';
	import Presentation from '$lib/Presentation.svelte';

	import { Magnifier } from 'svelte-magnifier';
	import RaspberryPi from '$lib/RaspberryPi.svelte';
import ModelChassis from '$lib/ModelChassis.svelte';
	let zoom_factor = tweened(1.5, {
		duration: 400,
		easing: expoOut
	});

	let y = 0;
	let headings = [];
	let presentation_mode;
	let waited = false;
	let inhibited = false;

	onMount(() => {
		const location = window.location.toString().split('#')[1];
		setTimeout(() => {
			if (location !== undefined) {
				scroll_to(location);
			} else {
				scroll_to('title-card');
			}
		}, 300);
		waited = true;
	});

	function scroll_next() {
		const location = window.location.toString().split('#')[1];
		if (location !== undefined) {
			for (let i = 0; i < headings.length; i++) {
				if (`#${location}` === headings[i].getAttribute('href')) {
					if (i + 1 !== headings.length) scroll_to(headings[i + 1].getAttribute('href'));
					break;
				}
			}
		} else {
			scroll_to(headings[0].getAttribute('href'));
		}
	}

	function scroll_prev() {
		const location = window.location.toString().split('#')[1];
		if (location !== undefined) {
			for (let i = 0; i < headings.length; i++) {
				if (`#${location}` === headings[i].getAttribute('href')) {
					if (i - 1 === -1) scroll_to('title-card');
					else scroll_to(headings[i - 1].getAttribute('href'));
					break;
				}
			}
		} else {
			scroll_to('title-card');
		}
	}

	function handle_keys(e) {
		if (e.key == 'ArrowRight' || e.key == 'ArrowDown' || e.key == ' ') {
			e.preventDefault();
			scroll_next();
			inhibited = false;
		} else if (e.key == 'ArrowLeft' || e.key == 'ArrowUp') {
			e.preventDefault();
			scroll_prev();
			inhibited = false;
		} else if (e.key == '.') {
			e.preventDefault();
			presentation_mode = presentation_mode ? false : true;
		} else if (e.key == '[') {
			e.preventDefault();
			zoom_factor.update((n) => {
				if (n - 1 <= 0) return n;
				else return n - 0.25;
			});
		} else if (e.key == ']') {
			e.preventDefault();
			zoom_factor.update((n) => n + 0.25);
		} else if (e.key == "'") {
			e.preventDefault();
			inhibited = inhibited ? false : true;
		}
	}

	function scroll_to(target) {
		target = target.toString().startsWith('#') ? target.toString() : `#${target.toString()}`;
		const el = document.querySelector(target);
		if (!el) return;
		window.scrollTo({ top: el.offsetTop, behavior: 'smooth' });
	}

	function replace_hash(new_hash: string) {
		const location = window.location.toString().split('#');
		if (location[1] !== undefined && location[1] !== new_hash.replace('#', ''))
			history.replaceState(null, null, location[0] + new_hash);
		else if (location[1] === undefined && new_hash !== '')
			history.replaceState(null, null, location[0] + new_hash);
	}
	$: if (waited) {
		if (y < 100) {
			replace_hash('');
		} else {
			for (let i = 0; i < headings.length; i++) {
				if (headings[i].offsetTop < y + 50 && headings[i].offsetTop > y - 50) {
					const heading = headings[i].getAttribute('href');
					replace_hash(heading);
					break;
				}
			}
		}
	}
</script>

<svelte:window on:keydown={handle_keys} bind:scrollY={y} />

<svelte:head>
	<title>Presentation 1 | TECBERRY.ml</title>
	<meta
		name="description"
		content="TEC modules for rapid and automated thermomechanical fatigue testing"
	/>
</svelte:head>

<Logo bind:headings />
<PageNumber bind:headings bind:presentation_mode />
<ScrollToSlide bind:headings bind:presentation_mode />
<Presentation bind:presentation_mode />
<Slide id_slide="title-card" short_name="" capstone={true} center={true} highlighted={true}>
	<svelte:fragment slot="slide-title">
		Design of a thermoelectric-based fatigue testing device
	</svelte:fragment>
	<svelte:fragment slot="byline">
		By Maryam K, Mohammed A, and Yaseen A <br /> Advised by Dr. Maen Alkhader
	</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<img
			alt="Industrial use of Raspberry Pi"
			src="/images/raspberry_industry.webp"
			style="position:relative; width: 100%; top: -20em; left: 0;z-index: -1; user-select: none"
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="introduction-to-fatigue" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">What is Thermal Fatigue?</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>Thermal fatigue testing types</li>
			<li>AUS Example</li>
			<li><a href="https://google.com">Google.com</a></li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="where-is-thermal-fatigue" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Where do you find Thermal Fatigue?</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>You may find thermal fatigue in many places.</p>
		<ul>
			<li>Thermal fatigue of aircraft components is a common occurrence</li>
			<li>
				Variation of the temperature field in turbines causes thermal stress on the turbine
				components
			</li>
			<li>The design of turbomachinery is directly related to the material performance</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="what-is-a-tec" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">What is a TEC module?</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>
			A thermoelectric, also known as a TEC or a Peltier module, is basically a heat pump. It
			operates on the principles of the Peltier effect, using electricity to move heat.
		</p>
		<TecModule
			width={420}
			height={420}
			bg_color="#cde6f2"
			cube_color="#ff3366"
			lights_color="#f2f2f2"
			style="float: right;"
			bind:inhibited
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="our-idea" bind:short_name={headings[headings.length]} capstone={true}>
	<svelte:fragment slot="slide-title">Our Idea</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Our idea is to use a bunch to heat and cool stuff to see if it breaks</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="the-raspberry-pi" bind:short_name={headings[headings.length]} capstone={false}>
	<svelte:fragment slot="slide-title">Automation & The Raspberry Pi</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>The Raspberry Pi is an incredibly versatile tool</p>
		<RaspberryPi
			width={480}
			height={400}
			bg_color="#cde6f2"
			cube_color="#ff3366"
			lights_color="#f2f2f2"
			style="float: right;"
			bind:inhibited
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="relevance-to-region" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">How is this relevant to the region?</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>
				Concrete fails often due to thermal fatigue from exposure to hot and moist environments
			</li>
			<li>UAE uses concrete in many buildings and infrastructure</li>
			<li>
				The UAE is home to one of the largest commercial plane hubs in the world, and the planes
				often see temperature variations of <em>-40°C to -60°C in the air</em>, and temperatures of
				<em>50°C on the ground</em>
			</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="environmental-impact" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Environmental Impact of our Project</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>
				Our project is a tool to create more sustainable materials that last longer and need less
				replacing
			</li>
			<li>Less materials needed to manufacture this than the larger machines</li>
			<li>Can study smaller specimens, unlike furnaces which need large specimens</li>
			<li>Larger furnaces waste heat by heating a larger chamber</li>
			<li>One drawback is that the Peltier effect is not very efficient</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="problem-statement" bind:short_name={headings[headings.length]} capstone={true}>
	<svelte:fragment slot="slide-title">Problem Statement</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p style="margin: 24px 0 0 64px; font-size: larger;text-align: justify;">
			There is a need for a small-scale, affordable, and quick thermal fatigue testing apparatus
			that is capable of being automated. The existence of thermoelectrics makes for an interesting
			solution to this identified need, as they are small, relatively affordable, and are easily
			automatable. The solution should be easy to set up and be as straightforward as possible, so
			it may be used as a tool for testing thermal fatigue for smaller research groups.
		</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="objectives" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Objectives</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p style="margin: 24px 0 0 64px; font-size: larger;text-align: justify;">
			Create a thermoelectric-based fatigue testing device that could endure a large number of
			cycles, collect data in an autonomous manner, and reach temperatures that are productive for
			the specimen studied.
		</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="preeminent-literature" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Literature Review</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Existing solutions</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="design-specs" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Product Design Specifications</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>
				Raise and lower temperature: -30°C to 70°C, which is within 30% of the thermoelectric
				specifications
			</li>
			<li>Do so within a reliable timeframe (specific cycle count and cycle time)</li>
			<li>Do so without destroying the thermoelectric (it's rated for a range and cyclecount)</li>
			<li>
				Allow us to carry out in-situ measurements - monitor the interfaces and damage due to
				fatigue in real-time
			</li>
			<li>The apparatus should do these tests autonomously with sparse supervision</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="cad-model" bind:short_name={headings[headings.length]} capstone={true}>
	<svelte:fragment slot="slide-title">CAD Model</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<Magnifier
			src="/images/chassis_drawing.png"
			width="700px"
			alt="AutoCAD drawing of chassis"
			mgShowOverflow={false}
			mgShape="square"
			mgWidth={250}
			mgHeight={250}
			className="chart_center_20"
			bind:zoomFactor={$zoom_factor}
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="cad-render" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">CAD Render</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ModelChassis
			width={620}
			height={500}
			bg_color="#cde6f2"
			cube_color="#ff3366"
			lights_color="#f2f2f2"
			style="margin: 0 0 0 20vw;"
			bind:inhibited
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="process-flow" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Process Flow</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<Magnifier
			src="/images/process_flow.png"
			width="700px"
			alt="Preliminary process flow diagram"
			mgShowOverflow={false}
			mgShape="square"
			mgWidth={250}
			mgHeight={250}
			className="chart_center_20"
			bind:zoomFactor={$zoom_factor}
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="wiring-diagram" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Wiring Diagram</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<Magnifier
			src="/images/wiring_diagram.png"
			width="500px"
			alt="Minimum viable wiring diagram"
			mgShowOverflow={false}
			mgShape="square"
			mgWidth={250}
			mgHeight={250}
			className="chart_center_30"
			bind:zoomFactor={$zoom_factor}
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="interactive-demo" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Demo Controls</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<Demo />
	</svelte:fragment>
</Slide>
<Slide id_slide="house-of-quality" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">House of Quality</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Make zoom into it</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="methodology" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Proposed methodology</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>Ensuring temperature uniformity in tested samples: Temperature analysis using Ansys</li>
			<li>
				Determining feasible heat cycle time: Conducting paramtric analysis and a heating/cooling
				Ansys simulation
			</li>
			<li>Designing a thermoelectric system</li>
			<li>
				Integrating a data collection system: Microcontroller, optical microscope, videography and
				thermal imaging
			</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="management" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Project Management: Distribution of Tasks</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<table style="margin: 24px 0 0 24px; font-size: x-large">
			<tr>
				<th>Task</th>
				<th />
				<th>Assignees</th>
			</tr>
			<tr>
				<td>Budgeting</td>
				<td>&#x2192;</td>
				<td>Mohammed &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Research, review</td>
				<td>&#x2192;</td>
				<td>Maryam, Mohammed &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Information Collection</td>
				<td>&#x2192;</td>
				<td>Maryam &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Information Collection</td>
				<td>&#x2192;</td>
				<td>Maryam &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Choosing most suitable equipment</td>
				<td>&#x2192;</td>
				<td>Mohammed &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Meeting minutes</td>
				<td>&#x2192;</td>
				<td>Maryam &#38; Mohammed</td>
			</tr>
			<tr>
				<td>Programming</td>
				<td>&#x2192;</td>
				<td>Mohammed &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Internal wiring connections</td>
				<td>&#x2192;</td>
				<td>Maryam &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Main assembly: CAD, Design</td>
				<td>&#x2192;</td>
				<td>Maryam, Mohammed &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Testing and Experimentation</td>
				<td>&#x2192;</td>
				<td>Maryam, Mohammed &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Website design & Documentation</td>
				<td>&#x2192;</td>
				<td>Yaseen</td>
			</tr>
			<tr>
				<td>3D Printing</td>
				<td>&#x2192;</td>
				<td>Maryam, Mohammed &#38; Yaseen</td>
			</tr>
			<tr>
				<td>Gantt Chart, House of Quality</td>
				<td>&#x2192;</td>
				<td>Maryam &#38; Mohammed</td>
			</tr>
		</table>
	</svelte:fragment>
</Slide>
<Slide id_slide="gantt-chart" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Gantt chart</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<Magnifier
			src="/images/gantt_chart.png"
			width="620px"
			alt="Gantt chart diagram"
			mgShowOverflow={false}
			mgShape="square"
			mgWidth={250}
			mgHeight={250}
			className="chart_center_20"
			bind:zoomFactor={$zoom_factor}
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="references" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">References</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Make zoom into it</p>
	</svelte:fragment>
</Slide>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
	}

	:global(.chart_center_20) {
		margin: 0 0 0 20vw;
	}

	:global(.chart_center_30) {
		margin: 0 0 0 30vw;
	}
</style>
