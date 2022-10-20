<script lang="ts">
	export let links,
		links_class = "";
</script>

<span class="relative">
	<div class="peer z-10 relative mx-2 cursor-pointer">
		<span
			class="font-medium select-none leading-3
		hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2">
			<slot name="title" />
		</span>
	</div>
	<span
		class="z-auto invisible peer-hover:visible hover:visible absolute grid scale-105 hover:scale-100 peer-hover:scale-100 transition-all will-change-transform  duration-300 opacity-0 peer-hover:opacity-100 hover:opacity-100
shadow-lg rounded w-full pb-4 bg-white dark:bg-slate-800 font-light {links_class}">
		{#each links as link}
			<a
				href={link.href}
				class="px-4 py-1.5 transition-colors duration-300 hover:bg-slate-200 dark:hover:bg-slate-600"
				>{link.text}</a>
		{/each}
	</span>
</span>
