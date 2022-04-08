<div class="flex h-full w-full">
	<div class="flex-col flex pr-10 pl-4 mr-4 pt-2 shadow h-full bg-slate-50 dark:bg-slate-800 dark:text-slate-50 ">
		<a href="/settings/account"  class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2">Account</a>
		<a href="/settings/admin"    class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2">Admin</a>
		<a href="/settings/security" class="hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2">Security</a>
	</div>
	<div class="mt-2">
		<slot />
	</div>
</div>
