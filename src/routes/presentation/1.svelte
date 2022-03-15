<script lang="ts">
	import { onMount } from 'svelte';
	import { tweened } from 'svelte/motion';
	import { expoOut } from 'svelte/easing';

	import Slide from '$lib/Slide.svelte';
	import Logo from '$lib/Logo.svelte';
	import TecModule from '$lib/TecModule.svelte';

	import PageNumber from '$lib/PageNumber.svelte';
	import ScrollToSlide from '$lib/ScrollToSlide.svelte';
	import Presentation from '$lib/Presentation.svelte';

	import { Magnifier } from 'svelte-magnifier';
	let zoom_factor = tweened(1.5, {
		duration: 400,
		easing: expoOut
	});

	let y = 0;
	let headings = [];
	let presentation_mode;
	let waited = false;

	onMount(() => {
		const location = window.location.toString().split('#')[1];
		if (location !== undefined) {
			scroll_to(location);
		} else {
			scroll_to('title-card');
		}
		waited = true;
	});

	function handle_keys(e) {
		if (e.key == 'ArrowRight' || e.key == 'ArrowDown' || e.key == ' ') {
			e.preventDefault();
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
		} else if (e.key == 'ArrowLeft' || e.key == 'ArrowUp') {
			e.preventDefault();
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
		} else if (e.key == '.') {
			presentation_mode = presentation_mode ? false : true;
		} else if (e.key == '-') {
			zoom_factor.update((n) => {
				if (n - 1 <= 0) return n;
				else return n - 1;
			});
		} else if (e.key == '=') {
			zoom_factor.update((n) => n + 1);
		}
	}

	function scroll_to(target) {
		target = target.toString().startsWith('#') ? target.toString() : `#${target.toString()}`;
		const el = document.querySelector(target);
		if (!el) return;
		el.scrollIntoView({
			behavior: 'smooth'
		});
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

<Logo bind:headings />
<PageNumber bind:headings bind:presentation_mode />
<ScrollToSlide bind:headings bind:presentation_mode />
<Presentation bind:presentation_mode />
<Slide id_slide="title-card" short_name="" capstone={true} center={true} highlighted={true}>
	<svelte:fragment slot="slide-title">
		TEC modules for rapid and automated thermomechanical fatigue testing
	</svelte:fragment>
	<svelte:fragment slot="byline">
		By Maryam K, Mohammed A, and Yaseen A <br /> Advised by Dr. Maen Alkhader
	</svelte:fragment>
	<svelte:fragment slot="slide-content">
			<img style="z-index:-2;width:100vw; position:absolute; top: 0px; left:0px" src="/images/raspberry_industry.webp" alt="A man looking at a Raspberry Pi in a lab">
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
			A TEC module, also known as a thermoelectric, or a Peltier module, is basically a heat pump.
		</p>
		<TecModule
			width={512}
			height={512}
			bg_color="#eeeeff"
			cube_color="#ff3366"
			lights_color="#99ffff"
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="our-idea" bind:short_name={headings[headings.length]} capstone={true}>
	<svelte:fragment slot="slide-title">Our Idea</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Our idea is to use a bunch to heat and cool stuff to see if it breaks</p>
		<Magnifier
			src="/android-chrome-512x512.png"
			width="256px"
			alt=""
			mgShowOverflow={false}
			bind:zoomFactor={$zoom_factor}
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
				The UAE is home to one of the largest commercial plane hubs in the word, and the planes
				often see temperatures of -40°C to -60°C in the air, and temperatures of 50°C on the ground.
			</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="environmental-impact" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Environmental Impact of our Project</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Big chambers = more big environmental</p>
		<ul>
			<li>
				Our project is a tool to create more sustainable materials that last longer and need less
				replacing
			</li>
			<li>Less materials needed to manufacture this than big machines</li>
			<li>Can study smaller specimens, unlike furnaces which need large specimens</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="problem-statement" bind:short_name={headings[headings.length]} capstone={true}>
	<svelte:fragment slot="slide-title">Problem Statement</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Problem</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="objectives" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Objectives</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Problem</p>
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
				Raise and lower temperature: -30°C to 70°C, which is within 30% of the TEC module
				specifications
			</li>
			<li>Do so within a reliable timeframe (specific cycle count and cycle time)</li>
			<li>Do so without destroying the TEC module (it's rated for a range and cyclecount)</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="cad-model" bind:short_name={headings[headings.length]} capstone={true}>
	<svelte:fragment slot="slide-title">CAD Model</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Put spinny here</p>
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
		<p>Make zoom into it</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="management" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Project Management</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Make zoom into it</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="gantt-chart" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Gant chart</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Make zoom into it</p>
	</svelte:fragment>
</Slide>
<Slide id_slide="references" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">References</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>Make zoom into it</p>
	</svelte:fragment>
</Slide>
