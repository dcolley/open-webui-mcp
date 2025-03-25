<script>
	import { onMount } from 'svelte';
  import { config, mcpServers, settings } from '$lib/stores';

	import MCPServers from '$lib/components/workspace/MCPServers.svelte';
</script>

<MCPServers />
