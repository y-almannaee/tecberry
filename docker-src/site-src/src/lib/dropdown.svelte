<script lang="ts">
	export let links,
		disabled,
		links_class = '';
</script>

<span class="relative">
	<div class="peer z-10 relative mx-2 cursor-default">
		<span
			tabindex="0"
			class="font-sans font-medium select-none leading-3
		hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
		>
			<slot name="title" />
		</span>
	</div>
	<span
		class="z-auto invisible 
		peer-focus-within:opacity-100 peer-focus-within:scale-100 peer-focus-within:visible
		peer-focus:opacity-100 peer-focus:scale-100 peer-focus:visible 
		peer-hover:opacity-100 peer-hover:scale-100 peer-hover:visible 
		hover:opacity-100 hover:scale-100 hover:visible
		focus:opacity-100 focus:scale-100 focus:visible
		focus-within:opacity-100 focus-within:scale-100 focus-within:visible
		absolute grid scale-105 
		transition-all will-change-transform duration-300 opacity-0 shadow-lg
		rounded w-full pb-4 bg-white dark:bg-slate-800 font-light {links_class}"
	>
		{#each links as link}
			<a
				href={link.href}
				on:click={(e) => {
					if (disabled) {
						e.preventDefault();
					}
				}}
				class:cursor-not-allowed={disabled}
				class="px-4 py-1.5 transition-colors hover:text-rose-700 hover:decoration-2 font-sans duration-300 hover:bg-slate-200 dark:hover:bg-slate-600"
				>{link.text}</a
			>
		{/each}
	</span>
</span>
