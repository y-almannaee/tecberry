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
				window.scrollTo({ top: 0, behavior: 'smooth' });
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
		<p style="float:left;display:inline-block">
			It is a severe fatigue failure phenomenon.<img
				src="/images/aus_damaged.webp"
				alt="Damage at AUS"
				style="float:right;display:inline-block;width:300px"
			/><br />
			Induced by cyclic (and usually routine) fluctuations in temperature on a structure<br /><br />
			What are the consequences?
		</p>
		<ul style="list-style-position: inside;display: inline-block;margin-top: -18em;">
			<li>Corrosion</li>
			<li>Cracking</li>
			<li>Occurence of maximum stresses beyond yielding</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="relation-aus" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">How does it relate to us?</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p style="float:left;display:inline-block">
			In AUS, the current tool of thermal fatigue testing is the INSTRON environmental chamber.<img
				src="/images/instron_man.png"
				alt="Man at AUS with an INSTRON chamber"
				style="float:right;display:inline-block;width:240px"
			/><br />
			Why not just use it everywhere?
		</p>
		<ul style="list-style-position: inside;display: inline-block;margin-top: -13em;">
			<li>Expensive</li>
			<li>Comes with a bulk of other functions</li>
			<li>Huge size</li>
			<li>Is not time efficient</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="where-is-thermal-fatigue" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Where do you find Thermal Fatigue?</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>In aerospace, thermal fatigue testing is critical and is a common occurance</p>
		<ul>
			<li>Fatigue damage is a root cause of failure in composite structures</li>

			<li>
				Variations of the temperature field in aircraft engine components causes thermal stresses to
				develop on them
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
			style="margin: 12px auto;display:block"
			bind:inhibited
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="problem-statement" bind:short_name={headings[headings.length]} capstone={true}>
	<svelte:fragment slot="slide-title">Problem Statement</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p style="margin: 24px 64px 0 64px;text-align: justify;">
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
		<p style="margin: 24px 64px 0 64px;text-align: justify;">
			Create a thermoelectric-based fatigue testing device that could endure a large number of
			cycles, collect data in an autonomous manner, and reach temperatures that are productive for
			the specimen studied.
		</p>
		<div style="margin: 16px auto;width:fit-content">
			<img src="/images/objective_fc.png" alt="Objective flow chart" style="width:720px" />
		</div>
	</svelte:fragment>
</Slide>
<Slide id_slide="the-raspberry-pi" bind:short_name={headings[headings.length]} capstone={false}>
	<svelte:fragment slot="slide-title">Automation & The Raspberry Pi</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>The Raspberry Pi is an incredibly versatile tool:</p>
		<ul>
			<li>Single-board computer or Microcontroller</li>
			<li>Capable of interfacing through its I/O</li>
			<li>Runs full computer operating system</li>
		</ul>
		<RaspberryPi
			width={480}
			height={400}
			bg_color="#cde6f2"
			cube_color="#ff3366"
			lights_color="#f2f2f2"
			style="margin: 12px auto;display:block"
			bind:inhibited
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="relevance-to-region" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">How is this relevant to the region?</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>Many roads in the UAE are made of poured concrete</li>
			<li>
				Concrete fails often due to thermal fatigue from exposure to hot and moist environments,
				like the UAE
			</li>
			<li>UAE uses concrete in many buildings and infrastructure</li>
			<li>
				The UAE is home to one of the largest commercial plane hubs in the world, and the planes
				often see temperature variations of <em>-40°C to -60°C in the air</em>, and temperatures of
				up to <em>50°C on the ground</em>
			</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="environmental-impact" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Environmental Impact of our Project</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>
				Our project is a tool to <em>create more sustainable materials</em> that last longer and need less
				replacing
			</li>
			<li><em>Less materials</em> needed to manufacture this than the larger machines</li>
			<li>Can <em>study smaller specimens</em>, unlike furnaces which need large specimens</li>
			<li>Larger furnaces waste heat by heating a larger chamber</li>
			<li>One drawback is that the Peltier effect is not very efficient</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="preeminent-literature" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Literature Review</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>
				Well type furnaces/environmental chambers are used to heat up the sample for a short period
				of time then remove it and let it cool for awhile and the process is repeated
			</li>
			<li>
				Conventional fatigue testing methods do not provide direct observations of how
				microstructures influence the fatigue life of the sample
			</li>
		</ul>
		<img
			width="240px"
			style="margin-right:64px; margin-left:64px"
			src="/images/furnace.jpg"
			alt="Well-Type furnace"
		/>
		<img width="320px" src="/images/moisture_chamber.jpg" alt="Moisture environmental chamber" />
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
		<p>
			The specimen is placed onto a plate with a suitable specific heat and conductivity in a sealed
			chamber.
		</p>
		<Magnifier
			src="/images/CAD_Drawing.jpg"
			width="850px"
			alt="AutoCAD drawing of chassis"
			mgShowOverflow={false}
			mgShape="square"
			mgWidth={250}
			mgHeight={250}
			className="chart_center_10"
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
			style="margin: 32px 0 0 20vw;"
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
			className="chart_center_20 chart_down_32"
			bind:zoomFactor={$zoom_factor}
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="wiring-diagram" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Wiring Diagram</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<p>
			A minimum viable connection between power supply, Raspberry Pi, H-bridge, and thermoelectrics
		</p>
		<Magnifier
			src="/images/wiring_diagram.png"
			width="400px"
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
		<Magnifier
			src="/images/house_of_quality.png"
			width="unset"
			height="90vh"
			alt="House of Quality"
			mgShowOverflow={false}
			mgShape="square"
			mgWidth={250}
			mgHeight={250}
			className="chart_center_20"
			bind:zoomFactor={$zoom_factor}
		/>
	</svelte:fragment>
</Slide>
<Slide id_slide="methodology" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Proposed methodology</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<ul>
			<li>
				Ensuring temperature uniformity in tested samples<span>
					Temperature analysis using Ansys</span
				>
			</li>
			<li>
				Determining feasible heat cycle time<span>
					Conducting paramtric analysis and a heating/cooling Ansys simulation</span
				>
			</li>
			<li>Designing a thermoelectric system</li>
			<li>
				Integrating a data collection system<span>
					Microcontroller, optical microscope, videography and thermal imaging</span
				>
			</li>
		</ul>
	</svelte:fragment>
</Slide>
<Slide id_slide="management" bind:short_name={headings[headings.length]}>
	<svelte:fragment slot="slide-title">Project Management: Distribution of Tasks</svelte:fragment>
	<svelte:fragment slot="slide-content">
		<table style="margin: 24px auto; font-size: x-large">
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
				<td>3D Printing/Chassis creation</td>
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
		<div class="csl-bib-body" style="line-height: 1.35; ">
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[1]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					L. Li, “9 - Effect of thermal fatigue on nonlinear damage behavior of ceramic-matrix
					composites,” in <i>Nonlinear Behavior of Ceramic-Matrix Composites</i>, L. Li, Ed.
					Woodhead Publishing, 2022, pp. 207-230. doi:
					<a href="https://doi.org/10.1016/B978-0-323-85770-3.00008-6"
						>10.1016/B978-0-323-85770-3.00008-6</a
					>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=urn%3Aisbn%3A978-0-323-85770-3&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&amp;rft.genre=bookitem&amp;rft.atitle=9%20-%20Effect%20of%20thermal%20fatigue%20on%20nonlinear%20damage%20behavior%20of%20ceramic%E2%80%93matrix%20composites&amp;rft.publisher=Woodhead%20Publishing&amp;rft.series=Woodhead%20Publishing%20Series%20in%20Composites%20Science%20and%20Engineering&amp;rft.aufirst=Longbiao&amp;rft.aulast=Li&amp;rft.au=Longbiao%20Li&amp;rft.au=Longbiao%20Li&amp;rft.date=2022-01-01&amp;rft.pages=207-230&amp;rft.spage=207&amp;rft.epage=230&amp;rft.isbn=978-0-323-85770-3&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[2]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					M. A. Eder, A. Sarhadi, and X. Chen, “A novel and robust method to quantify fatigue damage
					in fibre composite materials using thermal imagine analysis,” <i
						>International Journal of Fatigue</i
					>, vol. 150, p. 106326, Sep. 2021, doi:
					<a href="https://doi.org/10.1016/j.ijfatigue.2021.106326"
						>10.1016/j.ijfatigue.2021.106326</a
					>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=info%3Adoi%2F10.1016%2Fj.ijfatigue.2021.106326&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=A%20novel%20and%20robust%20method%20to%20quantify%20fatigue%20damage%20in%20fibre%20composite%20materials%20using%20thermal%20imagine%20analysis&amp;rft.jtitle=International%20Journal%20of%20Fatigue&amp;rft.stitle=International%20Journal%20of%20Fatigue&amp;rft.volume=150&amp;rft.aufirst=Martin%20A.&amp;rft.aulast=Eder&amp;rft.au=Martin%20A.%20Eder&amp;rft.au=Ali%20Sarhadi&amp;rft.au=Xiao%20Chen&amp;rft.date=2021-09-01&amp;rft.pages=106326&amp;rft.issn=0142-1123&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[3]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					J. I. Lee, L. Hu, P. Saha, and M. S. Kazimi, “Numerical analysis of thermal striping
					induced high cycle thermal fatigue in a mixing tee,” Nuclear Engineering and Design, vol.
					239, no. 5. Elsevier BV, pp. 833-839, May 2009. doi: 10.1016/j.nucengdes.2008.06.014. <a
						href="https://reader.elsevier.com/reader/sd/pii/S0029549308002987?token=B9315599253F65E47F66CB37DAEA2FBEBBDAD1F481D7117059516B6D200243E1D99674A7239C34777FC5CC602D027D8F&amp;originRegion=eu-west-1&amp;originCreation=20220308120817"
						>Available</a
					> (accessed Mar. 08, 2022).
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=doi%3A10.1016%2Fj.nucengdes.2008.06.014%20%7C%20Elsevier%20Enhanced%20Reader&amp;rft.identifier=https%3A%2F%2Freader.elsevier.com%2Freader%2Fsd%2Fpii%2FS0029549308002987%3Ftoken%3DB9315599253F65E47F66CB37DAEA2FBEBBDAD1F481D7117059516B6D200243E1D99674A7239C34777FC5CC602D027D8F%26originRegion%3Deu-west-1%26originCreation%3D20220308120817&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[4]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					H. Huang, M. An, Y. Wang, Z. Yu, and W. Ji, “Effect of environmental thermal fatigue on
					concrete performance based on mesostructural and microstructural analyses,” <i
						>Construction and Building Materials</i
					>, vol. 207, pp. 450-462, May 2019, doi:
					<a href="https://doi.org/10.1016/j.conbuildmat.2019.02.072"
						>10.1016/j.conbuildmat.2019.02.072</a
					>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=info%3Adoi%2F10.1016%2Fj.conbuildmat.2019.02.072&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Effect%20of%20environmental%20thermal%20fatigue%20on%20concrete%20performance%20based%20on%20mesostructural%20and%20microstructural%20analyses&amp;rft.jtitle=Construction%20and%20Building%20Materials&amp;rft.stitle=Construction%20and%20Building%20Materials&amp;rft.volume=207&amp;rft.aufirst=Hanfeng&amp;rft.aulast=Huang&amp;rft.au=Hanfeng%20Huang&amp;rft.au=Mingzhe%20An&amp;rft.au=Yue%20Wang&amp;rft.au=Ziruo%20Yu&amp;rft.au=Wenyu%20Ji&amp;rft.date=2019-05&amp;rft.pages=450-462&amp;rft.spage=450&amp;rft.epage=462&amp;rft.issn=09500618&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[5]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					Experimental and numerical study of crack initiation and propagation under a 3D thermal
					fatigue loading - ScienceDirect.<a
						href="https://www.sciencedirect.com/science/article/pii/S0142112307002575"> Available</a
					> (accessed Mar. 08, 2022).
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=Experimental%20and%20numerical%20study%20of%20crack%20initiation%20and%20propagation%20under%20a%203D%20thermal%20fatigue%20loading%20in%20a%20welded%20structure%20-%20ScienceDirect&amp;rft.identifier=https%3A%2F%2Fwww.sciencedirect.com%2Fscience%2Farticle%2Fpii%2FS0142112307002575"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[6]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					S. Li <i>et al.</i>, “Fatigue crack initiation behaviors around defects induced by welding
					thermal cycle in superalloy IN617B,” <i>International Journal of Fatigue</i>, vol. 158, p.
					106745, May 2022, doi:
					<a href="https://doi.org/10.1016/j.ijfatigue.2022.106745"
						>10.1016/j.ijfatigue.2022.106745</a
					>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=info%3Adoi%2F10.1016%2Fj.ijfatigue.2022.106745&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Fatigue%20crack%20initiation%20behaviors%20around%20defects%20induced%20by%20welding%20thermal%20cycle%20in%20superalloy%20IN617B&amp;rft.jtitle=International%20Journal%20of%20Fatigue&amp;rft.stitle=International%20Journal%20of%20Fatigue&amp;rft.volume=158&amp;rft.aufirst=Shanlin&amp;rft.aulast=Li&amp;rft.au=Shanlin%20Li&amp;rft.au=Qu%20Liu&amp;rft.au=Shao-Shi%20Rui&amp;rft.au=Xiaogang%20Li&amp;rft.au=Mengjia%20Hu&amp;rft.au=Kejian%20Li&amp;rft.au=Qixing%20Sun&amp;rft.au=Zhipeng%20Cai&amp;rft.au=Jiluan%20Pan&amp;rft.date=2022-05-01&amp;rft.pages=106745&amp;rft.issn=0142-1123&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[7]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					Dr. E. H. De Carlo, In-Situ Measuring Devices and Small Environmental Monitoring Systems
					p. 19. <a
						href="https://www.soest.hawaii.edu/oceanography/courses/OCN633/Fall%202013/SmallEnvMonitorSystemsA.pdf"
						>Available</a
					> (accessed Mar. 18, 2022).
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=In-Situ%20Measuring%20Devices%20and%20Small%20Environmental%20Monitoring%20Systems&amp;rft.pages=19&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[8]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					Investigation of thermal fatigue in fiber composite materials. Accessed: Mar. 12,
					2022. [Online].<a
						href="https://ntrs.nasa.gov/api/citations/19760020280/downloads/19760020280.pdf"
						>Available</a
					>
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=attachment&amp;rft.title=INVESTIGATION%20OF%20THERMAL%20FATIGUE%20IN%20FIBER%20COMPOSITE%20MATERIALS%20.pdf&amp;rft.identifier=https%3A%2F%2Fntrs.nasa.gov%2Fapi%2Fcitations%2F19760020280%2Fdownloads%2F19760020280.pdf"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[9]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					M. P. Boyce, “Materials,” in <i>Gas Turbine Engineering Handbook</i>, Elsevier, 2012, pp.
					493-514. doi:
					<a href="https://doi.org/10.1016/B978-0-12-383842-1.00011-1"
						>10.1016/B978-0-12-383842-1.00011-1</a
					>
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=urn%3Aisbn%3A978-0-12-383842-1&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&amp;rft.genre=bookitem&amp;rft.atitle=Materials&amp;rft.publisher=Elsevier&amp;rft.aufirst=Meherwan%20P.&amp;rft.aulast=Boyce&amp;rft.au=Meherwan%20P.%20Boyce&amp;rft.date=2012&amp;rft.pages=493-514&amp;rft.spage=493&amp;rft.epage=514&amp;rft.isbn=978-0-12-383842-1&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[10]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					N. R. Muktinutalapati, “Materials for Gas Turbines - An Overview,” <i
						>Advances in Gas Turbine Technology</i
					>, p. 24.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Materials%20for%20Gas%20Turbines%20%E2%80%93%20An%20Overview&amp;rft.jtitle=Advances%20in%20Gas%20Turbine%20Technology&amp;rft.aufirst=Nageswara%20Rao&amp;rft.aulast=Muktinutalapati&amp;rft.au=Nageswara%20Rao%20Muktinutalapati&amp;rft.pages=24&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[11]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					“Metallic grain structures and microscopic analysis insight | Struers.com.” <a
						href="https://www.struers.com/en/Knowledge/Materials/Metallic-grain-structures#characterization"
						>Available</a
					> (accessed Mar. 08, 2022).
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&amp;rft.type=webpage&amp;rft.title=Metallic%20grain%20structures%20and%20microscopic%20analysis%20insight%20%7C%20Struers.com&amp;rft.identifier=https%3A%2F%2Fwww.struers.com%2Fen%2FKnowledge%2FMaterials%2FMetallic-grain-structures%23characterization"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[12]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					“Microstructure and mechanical property of Al2O3f/SiO2 composites after fatigue tests”,
					[Online]. <a href="https://www.sciencedirect.com/science/article/pii/S2452213919301597"
						>Available</a
					>
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Microstructure%20and%20mechanical%20property%20of%20Al2O3f%2F%20SiO2%20composites%20after%20thermal%20shock%20and%20fatigue%20tests"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[13]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					D. H. Kim, K. K. Kim, K. B. Park, J. H. Yun, and C. S. Seok, “Prediction of thermal
					fatigue life based on the microstructure of thermal barrier coating applied to
					single-crystal CMSX-4 considering stress ratio,” <i>Ceramics International</i>, vol. 47,
					no. 15, pp. 21950-21958, Aug. 2021, doi:
					<a href="https://doi.org/10.1016/j.ceramint.2021.04.213">10.1016/j.ceramint.2021.04.213</a
					>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=info%3Adoi%2F10.1016%2Fj.ceramint.2021.04.213&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Prediction%20of%20thermal%20fatigue%20life%20based%20on%20the%20microstructure%20of%20thermal%20barrier%20coating%20applied%20to%20single-crystal%20CMSX-4%20considering%20stress%20ratio&amp;rft.jtitle=Ceramics%20International&amp;rft.stitle=Ceramics%20International&amp;rft.volume=47&amp;rft.issue=15&amp;rft.aufirst=D.%20H.&amp;rft.aulast=Kim&amp;rft.au=D.%20H.%20Kim&amp;rft.au=K.%20K.%20Kim&amp;rft.au=K.%20B.%20Park&amp;rft.au=J.%20H.%20Yun&amp;rft.au=C.%20S.%20Seok&amp;rft.date=2021-08-01&amp;rft.pages=21950-21958&amp;rft.spage=21950&amp;rft.epage=21958&amp;rft.issn=0272-8842&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[14]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					M. X. Zhang <i>et al.</i>, “Study on thermal fatigue behaviors of two kinds of vermicular
					graphite cast irons,” <i>Materials Science and Engineering: A</i>, vol. 814, p. 141212,
					May 2021, doi:
					<a href="https://doi.org/10.1016/j.msea.2021.141212">10.1016/j.msea.2021.141212</a>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=info%3Adoi%2F10.1016%2Fj.msea.2021.141212&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Study%20on%20thermal%20fatigue%20behaviors%20of%20two%20kinds%20of%20vermicular%20graphite%20cast%20irons&amp;rft.jtitle=Materials%20Science%20and%20Engineering%3A%20A&amp;rft.stitle=Materials%20Science%20and%20Engineering%3A%20A&amp;rft.volume=814&amp;rft.aufirst=M.%20X.&amp;rft.aulast=Zhang&amp;rft.au=M.%20X.%20Zhang&amp;rft.au=J.%20C.%20Pang&amp;rft.au=L.%20J.%20Meng&amp;rft.au=S.%20X.%20Li&amp;rft.au=Q.%20Y.%20Liu&amp;rft.au=A.%20L.%20Jiang&amp;rft.au=Z.%20F.%20Zhang&amp;rft.date=2021-05-13&amp;rft.pages=141212&amp;rft.issn=0921-5093&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[15]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					M. F. Cipière and J. A. Le Duff, “Thermal Fatigue Experience in French Piping: Influence
					of Surface Condition and Weld Local Geometry,” <i>Weld World</i>, vol. 46, no. 1-2, pp.
					23-27, Jan. 2002, doi:
					<a href="https://doi.org/10.1007/BF03266362">10.1007/BF03266362</a>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=info%3Adoi%2F10.1007%2FBF03266362&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Thermal%20Fatigue%20Experience%20in%20French%20Piping%3A%20Influence%20of%20Surface%20Condition%20and%20Weld%20Local%20Geometry&amp;rft.jtitle=Welding%20in%20the%20World&amp;rft.stitle=Weld%20World&amp;rft.volume=46&amp;rft.issue=1-2&amp;rft.aufirst=M.%20F.&amp;rft.aulast=Cipi%C3%A8re&amp;rft.au=M.%20F.%20Cipi%C3%A8re&amp;rft.au=J.%20A.%20Le%20Duff&amp;rft.date=2002-01&amp;rft.pages=23-27&amp;rft.spage=23&amp;rft.epage=27&amp;rft.issn=0043-2288%2C%201878-6669&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[16]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					L. Witek, D. Ngii, and T. Kowalski, “Thermal Fatigue Problems of Turbine Casing,” <i
						>Fatigue of Aircraft Structures</i
					>, vol. 2009, no. 1, Jan. 2009, doi:
					<a href="https://doi.org/10.2478/v10164-010-0018-6">10.2478/v10164-010-0018-6</a>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=info%3Adoi%2F10.2478%2Fv10164-010-0018-6&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Thermal%20Fatigue%20Problems%20of%20Turbine%20Casing&amp;rft.jtitle=Fatigue%20of%20Aircraft%20Structures&amp;rft.volume=2009&amp;rft.issue=1&amp;rft.aufirst=Lucjan&amp;rft.aulast=Witek&amp;rft.au=Lucjan%20Witek&amp;rft.au=Daniel%20Ngii&amp;rft.au=Tadeusz%20Kowalski&amp;rft.date=2009-01-26&amp;rft.issn=2081-7738&amp;rft.language=en"
			/>
			<div class="csl-entry" style="clear: left; ">
				<div
					class="csl-left-margin"
					style="float: left; padding-right: 0.5em;text-align: right; width: 2em;"
				>
					[17]
				</div>
				<div class="csl-right-inline" style="margin: 0 .4em 0 2.5em;">
					B. Salehnasab, J. Marzbanrad, and E. Poursaeidi, “Transient thermal fatigue crack
					propagation prediction in a gas turbine component,” <i>Engineering Failure Analysis</i>,
					vol. 130, p. 105781, Dec. 2021, doi:
					<a href="https://doi.org/10.1016/j.engfailanal.2021.105781"
						>10.1016/j.engfailanal.2021.105781</a
					>.
				</div>
			</div>
			<span
				class="Z3988"
				title="url_ver=Z39.88-2004&amp;ctx_ver=Z39.88-2004&amp;rfr_id=info%3Asid%2Fzotero.org%3A2&amp;rft_id=info%3Adoi%2F10.1016%2Fj.engfailanal.2021.105781&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.atitle=Transient%20thermal%20fatigue%20crack%20propagation%20prediction%20in%20a%20gas%20turbine%20component&amp;rft.jtitle=Engineering%20Failure%20Analysis&amp;rft.stitle=Engineering%20Failure%20Analysis&amp;rft.volume=130&amp;rft.aufirst=B.&amp;rft.aulast=Salehnasab&amp;rft.au=B.%20Salehnasab&amp;rft.au=J.%20Marzbanrad&amp;rft.au=E.%20Poursaeidi&amp;rft.date=2021-12-01&amp;rft.pages=105781&amp;rft.issn=1350-6307&amp;rft.language=en"
			/>
		</div>
	</svelte:fragment>
</Slide>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		width: fit-content;
	}

	:global(.chart_center_20) {
		margin: 0 0 0 20vw;
	}

	:global(.chart_center_30) {
		margin: 0 0 0 30vw;
	}

	:global(.chart_center_10) {
		margin: 0 0 0 10vw;
	}

	:global(.chart_down_32) {
		margin-top: 32px;
	}

	li span::before {
		content: '\a\21B3';
		white-space: pre;
	}

	li span {
		font-size: 1.6rem;
	}

	li {
		font-size: 1.9rem;
		line-height: 2;
	}

	p {
		font-size: 1.9rem;
	}

	em {
		font-style: normal;
		font-weight: 700;
		font-family: 'Work Sans', 'Trebuchet MS', sans-serif;
		color: var(--main);
		font-size: 2rem;
	}
</style>
