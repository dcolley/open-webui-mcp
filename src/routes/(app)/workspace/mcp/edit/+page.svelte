<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { getToolById, getTools, updateToolById } from '$lib/apis/tools';
	import Spinner from '$lib/components/common/Spinner.svelte';
	// import ToolkitEditor from '$lib/components/workspace/Tools/ToolkitEditor.svelte';
	import MCPServerEditor from '$lib/components/workspace/MCPServers/MCPServerEditor2.svelte';
	import { updateMCPServerById, getMCPServerById } from '$lib/apis/mcp';
	import { WEBUI_VERSION } from '$lib/constants';
	import { tools } from '$lib/stores';
	import { compareVersion, extractFrontmatter } from '$lib/utils';
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';

	const i18n = getContext('i18n');

	let server = null;

	const saveHandler = async (data) => {
		console.log('saveHandler', data);

		// const manifest = extractFrontmatter(data.content);
		// if (compareVersion(manifest?.required_open_webui_version ?? '0.0.0', WEBUI_VERSION)) {
		// 	console.log('Version is lower than required');
		// 	toast.error(
		// 		$i18n.t(
		// 			'Open WebUI version (v{{OPEN_WEBUI_VERSION}}) is lower than required version (v{{REQUIRED_VERSION}})',
		// 			{
		// 				OPEN_WEBUI_VERSION: WEBUI_VERSION,
		// 				REQUIRED_VERSION: manifest?.required_open_webui_version ?? '0.0.0'
		// 			}
		// 		)
		// 	);
		// 	return;
		// }

		// const res = await updateToolById(localStorage.token, tool.id, {
		// 	id: data.id,
		// 	name: data.name,
		// 	meta: data.meta,
		// 	content: data.content,
		// 	access_control: data.access_control
		// }).catch((error) => {
		// 	toast.error(`${error}`);
		// 	return null;
		// });
    const res = await updateMCPServerById(localStorage.token, data.id, {
      id: data.id,
      name: data.name,
      description: data.description,
      type: data.type,
      command: data.command,
      url: data.url,
			valves: data.valves,
			enabled: data.enabled
		}).catch((error) => {
			toast.error(`${error}`);
			return null;
		});

		if (res) {
			toast.success($i18n.t('Tool updated successfully'));
			tools.set(await getTools(localStorage.token));

			// await goto('/workspace/tools');
		}
	};

	onMount(async () => {
		console.log('mounted');
		const id = $page.url.searchParams.get('id');

		if (id) {
			server = await getMCPServerById(localStorage.token, id).catch((error) => {
				toast.error(`${error}`);
				goto('/workspace/mcp');
				return null;
			});

			console.log(server);
		}
	});
</script>

{#if server}
	<MCPServerEditor
		edit={true}
		id={server.id}
		name={server.name}
		description={server.description}
		type={server.type}
		command={server.command}
		url={server.url}
		valves={server.valves}
		enabled={server.enabled}
		accessControl={server.access_control}
		onSave={(value) => {
			saveHandler(value);
		}}
	/>
{:else}
	<div class="flex items-center justify-center h-full">
		<div class=" pb-16">
			<Spinner />
		</div>
	</div>
{/if}
