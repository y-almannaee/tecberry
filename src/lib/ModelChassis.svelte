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
		scale_c = 760;

	const clock = new THREE.Clock();
	let delta = 0,
		interval = 1 / 30;
	// camera = new THREE.PerspectiveCamera(40, width / height, 100, 100);
	camera = new THREE.OrthographicCamera(
		width / -scale_c,
		width / scale_c,
		height / scale_c,
		height / -scale_c,
		0.01,
		10
	);
	camera.position.set(1, 1, 1);
	camera.lookAt(0, 0, 0);
	camera.near = 0.9;
	camera.up.set(0, 1, 0);

	scene = new THREE.Scene();
	scene.background = new THREE.Color(bg_color);

	// LOAD PI GLB
	const loader = new GLTFLoader();
	let CAD_MODEL;

	loader.load(
		'/CAD_Model.glb',
		function (gltf) {
			CAD_MODEL = gltf.scene;
			//enable_shadows(CAD_MODEL);
			gltf.scene.traverse((child) => {
				if (child.castShadow === false || child.recieveShadow === false) {
					child.castShadow = true;
					child.recieveShadow = true;
				}
			});
			CAD_MODEL.scale.set(1.6, 1.6, 1.6);
			CAD_MODEL.position.set(0,-0.1,0);
			scene.add(gltf.scene);
			console.log(gltf.animations);
			console.log(gltf.scene);
			console.log(gltf.scenes);
			console.log(gltf.cameras);
			console.log(gltf.asset);
		},
		function (xhr) {
			console.log((xhr.loaded / xhr.total) * 100 + '% loaded of CAD.glb');
		},
		function (error) {
			console.log('An error has occurred loading CAD.glb');
			console.error(error);
		}
	);

	const geometry = new THREE.BoxGeometry();
	const material = new THREE.MeshPhongMaterial({
		color: new THREE.Color(cube_color)
	});
	const cube = new THREE.Mesh(geometry, material);
	//scene.add(cube);

	const light = new THREE.AmbientLight(new THREE.Color(bg_color), 0.2);

	const directional_lights = [];

	for (let i = 0; i < 2; i++) {
		let directional_light = new THREE.DirectionalLight(new THREE.Color(lights_color), 0.7);
		directional_light.castShadow = true;
		directional_light.shadow.mapSize.width = 1024;
		directional_light.shadow.mapSize.height = 1024;
		directional_light.shadow.camera.near = 0.1;
		directional_light.shadow.camera.far = 20;
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

	// const axesHelper = new THREE.AxesHelper(5);
	// scene.add(axesHelper);

	scene.add(light);

	const framelock_animate = () => {
		if (do_rotation && !inhibited) {
			if (CAD_MODEL !== undefined) CAD_MODEL.rotation.y += 0.005;
		}
		renderer.render(scene, camera);
	};

	const animate = () => {
		if (!inhibited) requestAnimationFrame(animate);
		delta += clock.getDelta();
		if (delta > interval) {
			framelock_animate();
			delta %= interval;
		}
	};

	const resize = () => {
		if (!renderer) return;
		renderer.setSize(width, height);
		camera.aspect = width / height;
		camera.updateProjectionMatrix();
		renderer.setPixelRatio(window.devicePixelRatio);
	};

	const create_scene = (el) => {
		renderer = new THREE.WebGLRenderer({
			logarithmicDeptherBuffer: true,
			antialias: true,
			alpha: true,
			canvas: el
		});
		renderer.shadowMap.enabled = true;
		renderer.shadowMap.type = THREE.VSMShadowMap;
		renderer.outputEncoding = THREE.sRGBEncoding; // required by GLTFLoader

		arcball_controls = new ArcballControls(camera, el, scene);
		arcball_controls.setGizmosVisible(false);
		arcball_controls.addEventListener('change', animate);
		resize();
		renderer.setPixelRatio(window.devicePixelRatio);
		animate();
	};

	onMount(() => {
		create_scene(el);
	});

	$: {
		inhibited = inhibited;
		resize();
		setTimeout(resize, 1500);
	}
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
