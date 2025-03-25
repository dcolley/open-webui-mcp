<script>
	import { v4 as uuidv4 } from 'uuid';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import { config, mcpServers, settings } from '$lib/stores';

	import { onMount, tick, getContext } from 'svelte';
	import { createNewMCPServer, getMCPServerById } from '$lib/apis/mcp';
	import { getMCPServers } from '$lib/apis/mcp';

	import MCPServerEditor from '$lib/components/workspace/MCPServers/MCPServerEditor2.svelte';

	const i18n = getContext('i18n');

	const onSave = async (serverInfo) => {
		console.log('onSubmit', serverInfo);
		// if (!$mcpServers) { $mcpServers = []; }
		if ($mcpServers?.find((s) => s.id === serverInfo.id)) {
			toast.error(
				`Error: A server with the ID '${serverInfo.id}' already exists. Please select a different ID to proceed.`
			);
			return;
		}

		if (serverInfo.id === '') {
			toast.error('Error: Server ID cannot be empty. Please enter a valid ID to proceed.');
			return;
		}

		if (serverInfo) {
			const res = await createNewMCPServer(localStorage.token, {
				...serverInfo,
				// meta: {
				// 	...serverInfo.meta,
				// 	profile_image_url: serverInfo.meta.profile_image_url ?? '/static/favicon.png',
				// 	suggestion_prompts: serverInfo.meta.suggestion_prompts
				// 		? serverInfo.meta.suggestion_prompts.filter((prompt) => prompt.content !== '')
				// 		: null
				// },
				// params: { ...serverInfo.params }
			}).catch((error) => {
				toast.error(`${error}`);
				return null;
			});

			if (res) {
				await mcpServers.set(
					await getMCPServers(
						localStorage.token,
						$config?.features?.enable_direct_connections && ($settings?.directConnections ?? null)
					)
				);
				toast.success($i18n.t('Server created successfully!'));
				await goto('/workspace/mcp');
			}
		}
	};

	let server = null;

	onMount(async () => {
		window.addEventListener('message', async (event) => {
			if (
				!['https://openwebui.com', 'https://www.openwebui.com', 'http://localhost:5173'].includes(
					event.origin
				)
			) {
				return;
			}

			let data = JSON.parse(event.data);

			if (data?.info) {
				data = data.info;
			}

			server = data;
		});

		if (window.opener ?? false) {
			window.opener.postMessage('loaded', '*');
		}

		if (sessionStorage.model) {
			server = JSON.parse(sessionStorage.server);
			sessionStorage.removeItem('server');
		}
	});
</script>

{#key server}
	<MCPServerEditor {server} {onSave} />
{/key}
