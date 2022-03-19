<script lang="ts">
	import { onMount } from 'svelte';

	export let width, height, bg_color, cube_color, lights_color, inhibited;
	import * as THREE from 'three';
	import { ArcballControls } from 'three/examples/jsm/controls/ArcballControls.js';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

	let camera,
		scene,
		renderer,
		el,
		arcball_controls,
		do_rotation = true,
		scale_c = 700;

	const clock = new THREE.Clock();
	let delta = 0,
		interval = 1 / 60;
	camera = new THREE.OrthographicCamera(
		width / -scale_c,
		width / scale_c,
		height / scale_c,
		height / -scale_c,
		0.01,
		10
	);
	camera.position.set(-0.4, 1, 1);
	camera.lookAt(0, 0, 0);
	camera.up.set(-1 -0.5, 0);

	scene = new THREE.Scene();
	scene.background = new THREE.Color(bg_color);

	// LOAD TEC MODULE GLB
	const loader = new GLTFLoader();
	let TEC;

	loader.load(
		'/Peltier.glb',
		function (gltf) {
			TEC = gltf.scene;
			gltf.scene.traverse((child) => {
				if (child.castShadow === false || child.recieveShadow === false) {
					child.castShadow = true;
					child.recieveShadow = true;
				}
			});
			TEC.scale.set(10, 10, 10);
			scene.add(gltf.scene);
			console.log(gltf.animations);
			console.log(gltf.scene);
			console.log(gltf.scenes);
			console.log(gltf.cameras);
			console.log(gltf.asset);
		},
		function (xhr) {
			console.log((xhr.loaded / xhr.total) * 100 + '% loaded of Peltier.glb');
		},
		function (error) {
			console.log('An error has occurred loading Peltier.glb');
			console.error(error);
		}
	);

	const geometry = new THREE.BoxGeometry();
	const material = new THREE.MeshPhongMaterial({
		color: new THREE.Color(cube_color)
	});
	const cube = new THREE.Mesh(geometry, material);
	//scene.add(cube);

	const light = new THREE.AmbientLight(new THREE.Color(bg_color), 0.3);

	const directional_lights = [];

	for (let i = 0; i < 2; i++) {
		let directional_light = new THREE.DirectionalLight(new THREE.Color(lights_color), 0.6);
		directional_light.shadowCameraVisible = true;
		directional_light.castShadow = true;
		let x: number, y: number, z: number;
		switch (i) {
			case 0:
				x = 1;
				y = 1;
				z = 1;
				break;
			case 1:
				x = 0;
				y = 1;
				z = 1.5;
				break;
		}
		directional_light.position.set(x, y, z);
		directional_light.target.position.set(0, 0, 0);
		scene.add(directional_light);
		scene.add(directional_light.target);
		directional_lights.push(directional_light);
	}
	cube.castShadow = true;
	cube.receiveShadow = true;

	const axesHelper = new THREE.AxesHelper(5);
	scene.add(axesHelper);

	scene.add(light);

	const framelock_animate = () => {
		if (do_rotation && !inhibited) {
			if (TEC !== undefined) {
				// TEC.rotation.y += 0.005;
				TEC.rotation.x += 0.002;
			}
		}
		renderer.render(scene, camera);
	};

	const animate = () => {
		requestAnimationFrame(animate);
		delta += clock.getDelta();
		if (delta > interval) {
			framelock_animate();
			delta %= interval;
		}
	};

	const resize = () => {
		renderer.setSize(width, height);
		camera.aspect = width / height;
		camera.updateProjectionMatrix();
	};

	const create_scene = (el) => {
		renderer = new THREE.WebGLRenderer({
			antialias: true,
			alpha: true,
			canvas: el
		});
		renderer.shadowMap.enabled = true;
		renderer.shadowMap.type = THREE.VSMShadowMap;
		renderer.outputEncoding = THREE.sRGBEncoding; // required by GLTFLoader
		arcball_controls = new ArcballControls(camera, el, scene);
		arcball_controls.setGizmosVisible(false);
		resize();
		renderer.setPixelRatio(window.devicePixelRatio);
		animate();
	};

	onMount(() => {
		create_scene(el);
	});
</script>

<svelte:window on:resize={resize} />

<canvas
	{width}
	{height}
	bind:this={el}
	on:pointerdown={() => {
		do_rotation = false;
	}}
	on:pointerup={() => {
		do_rotation = true;
	}}
	{...$$restProps}
>
	Your browser does not support this element.
</canvas>
