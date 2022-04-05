<script>
	import "../app.css";
</script>

<div class="flex flex-col h-screen justify-between">
	<header class="">
		<a href="/login">Login</a>
	</header>
	<main class="mb-auto">
		<slot />
	</main>
	<footer class="p-4 mx-auto md:flex md:items-center md:justify-between md:p-6">
		<span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">
			© 2022 <a
				href="https://yaseen.ae"
				class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
				>Yaseen AlMannaee</a>
			<br /> Built with
			<a
				class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
				href="https://kit.svelte.dev">
				SvelteKit
			</a>
			and
			<a
				class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
				href="https://tailwindcss.com">TailwindCSS</a>
		</span>
		<!-- <ul class="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0">
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6 ">About</a>
				</li>
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6">Privacy Policy</a>
				</li>
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6">Licensing</a>
				</li>
				<li>
					<a href="#" class="hover:underline">Contact</a>
				</li>
			</ul> -->
	</footer>
</div>
