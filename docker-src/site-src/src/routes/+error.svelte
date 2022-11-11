<script>
	import { page } from '$app/stores';
</script>

Error {$page.status}

{$page.error.message}