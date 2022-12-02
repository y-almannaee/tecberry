<script>
	import { Avatar } from '@skeletonlabs/skeleton';
	import { LogIn } from 'lucide-svelte';

	export let classes = '';
	export let classes_icon = '';
	export let userdata = { loggedIn: false };
</script>

{#if userdata.loggedIn}
	<a href="/settings/account" class={classes}>
		{#if userdata && userdata.pfp}
			<div
				class="{classes_icon} rounded-full overflow-hidden bg-slate-50 fill-red-700 border-2 border-black transition-colors duration-300 hover:!border-red-700"
			>
				<img class="h-full w-auto" referrerpolicy="no-referrer" alt="" src={userdata.pfp} />
			</div>
		{:else}
			<Avatar
				width={classes_icon}
				background="bg-slate-50"
				fill="fill-red-700"
				border="border-2 border-black transition-colors duration-300 hover:!border-red-700"
				initials={userdata.name.match(/\b(\w)/g).join('')}
			/>
		{/if}
	</a>
{:else}
	<a href="/login" class={classes}>
		<LogIn
			class="{classes_icon} transition-colors duration-300 transition-colors duration-300 hover:text-[#f36] rounded"
		/>
	</a>
{/if}
