<div class="flex h-full w-full pt-8 md:pt-10 lg:pt-11">
	<div
		class="flex-col flex fixed pr-10 pl-4 pt-2 shadow-xl z-10 h-screen max-w-[12rem] bg-white dark:bg-slate-800 dark:text-slate-50 "
	>
		<slot name="pane"/>
	</div>
	<div
		class="flex-col invisible flex pr-10 pl-4 pt-2 shadow-xl z-10 h-full bg-white dark:bg-slate-800 dark:text-slate-50 "
	>
		<slot name="pane"/>
	</div>
	<div class="bg-gray-50 dark:bg-slate-900 h-full w-full pl-4">
		<slot name="main"/>
	</div>
</div>
