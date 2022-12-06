<script lang="ts">
	import { FolderOpen } from "lucide-svelte";
	import { ArrowDownRight } from "lucide-svelte";
	import { fly } from "svelte/transition";
	import { onMount } from "svelte";
	import Tripanel from "$lib/tripanel.svelte";

	let doneanimate=false,
		markdown,
		scripts_fetched = 0,
		scripts = [],
		documents = [],
		directories = [];

	function display_md(text) {
		let converter = new showdown.Converter({
				simplifiedAutoLink: true,
				tables: true
			}),
			html = converter.makeHtml(text);
		markdown.innerHTML = html;
	}

	async function get_text_from_url(url) {
		return new Promise((resolve, reject) => {
			fetch(url).then((res) => {
				res.text().then((text) => {
					resolve(text);
				});
			});
		});
	}

	function scour_directory(url, default_dir = undefined) {
		default_dir = default_dir || url;
		fetch(url).then((res) => {
			res.json().then(async (json_res) => {
				for (const item of json_res) {
					const name = item.name
						.split(".")[0]
						.replace(/[^a-z0-9]/gi, "-")
						.toLowerCase();
					const directory_name = url
						.replace(default_dir + "/", "")
						.replace(/[^a-z0-9]/gi, "-")
						.toLowerCase();
					if (item.type == "file") {
						const push_to =
							url === default_dir ? documents : directories[directories.length - 1].documents;
						push_to.push({
							id: `${name}-${documents.length}`,
							name:
								item.name.split(".")[0].charAt(0).toUpperCase() +
								item.name.split(".")[0].substring(1),
							href: url + "/" + item.name
						});
					}
					if (item.type == "directory" && url === default_dir) {
						directories.push({
							id: `${name}-${directories.length}`,
							name: item.name.charAt(0).toUpperCase() + item.name.substring(1),
							documents: []
						});
						await scour_directory(default_dir + "/" + item.name, default_dir);
					}
					console.log(documents);
					console.log(directories);
					documents = documents;
					directories = directories;
				}
			});
		});
	}

	async function enter() {
		await scour_directory("/docs");
		//display_md(await get_text_from_url("/docs/default.md"));
	}

	onMount(async () => {
		for (const script of scripts) {
			console.log(script);
			script.addEventListener("load", async () => {
				console.log("loaded");
				scripts_fetched += 1;
			});

			script.addEventListener("error", (event) => {
				console.error("something went wrong", event);
				console.log("error");
			});
		}
	});

	$: if ((scripts_fetched = scripts.length)) {
		enter();
	}
</script>

<svelte:head>
	<title>Documentation | TECBERRY.ml</title>

	<script
		bind:this={scripts[scripts.length]}
		src="https://cdnjs.cloudflare.com/ajax/libs/showdown/2.0.3/showdown.min.js"
		integrity="sha512-vx8rJNrYIZPDr290AV2tL04x0CKjLHSnTXrHMeb1kqbhfGwBnclPDOWIWxRiVS6Oe1oGzk5MzNz/eLzVku30kg=="
		crossorigin="anonymous"
		referrerpolicy="no-referrer"></script>
	<!--<script
		bind:this={scripts[scripts.length]}
		src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.0/highlight.min.js"
		integrity="sha512-BNc7saQYlxCL10lykUYhFBcnzdKMnjx5fp5s5wPucDyZ7rKNwCoqJh1GwEAIhuePEK4WM9askJBRsu7ma0Rzvg=="
		crossorigin="anonymous"
		referrerpolicy="no-referrer"></script>-->
</svelte:head>

<!--<div class="flex h-full w-full">
	<div
		class="flex-col flex pr-10 pl-4 pt-2 shadow-xl z-10 h-full bg-white dark:bg-slate-800 dark:text-slate-50 ">
		{#each directories as dir (dir.id)}
			<div class="font-semibold">
				<span><FolderOpen class="h-6 w-6 inline align-bottom mr-1" />{dir.name}</span>
				<div class="font-light ml-6">
					{#each dir.documents as document (document.id)}
						<ArrowDownRight class="h-6 w-6 inline align-bottom mr-1" />
						<a
							href="#{dir.id}_{document.id}"
							on:click={async () => {
								display_md(await get_text_from_url(document.href));
							}}
							class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
							>{document.name}</a>
					{/each}
				</div>
			</div>
		{/each}
		{#each documents as document (document.id)}
			<a
				href="#{document.id}"
				on:click={async () => {
					display_md(await get_text_from_url(document.href));
				}}
				class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
				>{document.name}</a>
		{/each}
		{#if directories.length == 0 && documents.length == 0}
			<p class="text-xs mt-4 italic text-slate-400">There is no documentation here...</p>
		{/if}
	</div>
	<div class="bg-gray-50 dark:bg-slate-900 h-full w-full pl-4 {doneanimate?"overflow-y-hidden":"overflow-y-clip"}">
		<div
			in:fly={{delay: 300, duration: 600, x: 0, y: 500, opacity: 0}}
			on:introend="{()=>{doneanimate=true}}"
			class="aspect-[70/99] px-6 py-12 my-4 mx-2 bg-white shadow-xl shadow-slate-700/10 dark:shadow-slate-50/10 ring-1 ring-gray-900/5 dark:ring-white/5 md:max-w-3xl md:mx-auto lg:max-w-4xl lg:pt-16 lg:pb-28">
			<div
				bind:this={markdown}
				class="max-w-prose mx-auto lg:text-lg prose prose-rose lg:prose-lg" />
		</div>
	</div>
</div>-->

<Tripanel>
	<svelte:fragment slot="pane">
		{#each directories as dir (dir.id)}
			<div class="font-semibold">
				<span><FolderOpen class="h-6 w-6 inline align-bottom mr-1" />{dir.name}</span>
				<div class="font-light ml-6">
					{#each dir.documents as document (document.id)}
						<ArrowDownRight class="h-6 w-6 inline align-bottom mr-1" />
						<a
							href="#{dir.id}_{document.id}"
							on:click={async () => {
								display_md(await get_text_from_url(document.href));
							}}
							class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
							>{document.name}</a>
					{/each}
				</div>
			</div>
		{/each}
		{#each documents as document (document.id)}
			<a
				href="#{document.id}"
				on:click={async () => {
					display_md(await get_text_from_url(document.href));
				}}
				class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
				>{document.name}</a>
		{/each}
		{#if directories.length == 0 && documents.length == 0}
			<p class="font-sans pt-2 !text-xs italic !text-slate-400">There is no documentation here...</p>
		{/if}
	</svelte:fragment>
	<svelte:fragment slot="main">
		<span class="w-full h-full p-0 m-0 {doneanimate?"overflow-y-hidden":"overflow-y-clip"}">
		<div
			in:fly={{delay: 300, duration: 600, x: 0, y: 500, opacity: 0}}
			on:introend="{()=>{doneanimate=true}}"
			class="aspect-[70/99] px-6 py-12 my-4 mx-2 bg-white shadow-xl shadow-slate-700/10 dark:shadow-slate-50/10 ring-1 ring-gray-900/5 dark:ring-white/5 md:max-w-3xl md:mx-auto lg:max-w-4xl lg:pt-16 lg:pb-28">
			<div
				bind:this={markdown}
				class="max-w-prose mx-auto lg:text-lg prose prose-rose lg:prose-lg" />
		</div>
		</span>
	</svelte:fragment>
</Tripanel>