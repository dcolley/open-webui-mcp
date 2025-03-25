<script lang="ts">
	import { getContext, onMount, tick } from 'svelte';

	const i18n = getContext('i18n');

	import CodeEditor from '$lib/components/common/CodeEditor.svelte';
	import { goto } from '$app/navigation';
	import ConfirmDialog from '$lib/components/common/ConfirmDialog.svelte';
	import Badge from '$lib/components/common/Badge.svelte';
	import ChevronLeft from '$lib/components/icons/ChevronLeft.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import LockClosed from '$lib/components/icons/LockClosed.svelte';
	import AccessControlModal from '../common/AccessControlModal.svelte';

	let formElement = null;
	let loading = false;

	let showConfirm = false;
	let showAccessControlModal = false;

	export let edit = false;
	export let clone = false;

	export let onSave = (data: any) => {};
	// export let onSubmit = (data: any) => {};

	export let id = '';
	export let name = '';
	export let description = '';
	export let type = 'sse';
	export let command = '';
	export let url = '';
	export let valves = [];
	export let enabled = true;

  export let accessControl = null;

	// let _content = '';
	// $: if (content) {
	// 	updateContent();
	// }

	// const updateContent = () => {
	// 	_content = content;
	// };

	$: if (name && !edit && !clone) {
		id = name.replace(/\s+/g, '_').toLowerCase();
	}

	//let codeEditor;
	//let boilerplate = ``;

	const saveHandler = async () => {
		console.log('saveHandler');
		loading = true;
		onSave({
			id,
			name,
			description,
			type,
			command,
			url,
			valves,
			enabled,
			access_control: accessControl
		});
	};

	// const submitHandler = async () => {
	// 	console.log('submitHandler');
	// 	// if (codeEditor) {
	// 	// 	content = _content;
	// 	// 	await tick();

	// 	// 	const res = await codeEditor.formatPythonCodeHandler();
	// 	// 	await tick();

	// 	// 	content = _content;
	// 	// 	await tick();

	// 	// 	if (res) {
	// 	// 		console.log('Code formatted successfully');

	// 	// 		saveHandler();
	// 	// 	}
	// 	// }
	// 	await saveHandler();
	// };
</script>

<AccessControlModal
	bind:show={showAccessControlModal}
	bind:accessControl
	accessRoles={['read', 'write']}
/>

<div class=" flex flex-col justify-between w-full overflow-y-auto h-full">
	<div class="mx-auto w-full md:px-0 h-full">
		<form
			bind:this={formElement}
			class=" flex flex-col max-h-[100dvh] h-full"
			on:submit|preventDefault={() => {
				// if (edit) {
					saveHandler();
				// } else {
				// 	showConfirm = true;
				// }
			}}
		>
			<div class="flex flex-col flex-1 overflow-auto h-0 rounded-lg">
				<div class="w-full mb-2 flex flex-col gap-0.5">
					<div class="flex w-full items-center">
						<div class=" shrink-0 mr-2">
							<Tooltip content={$i18n.t('Back')}>
								<button
									class="w-full text-left text-sm py-1.5 px-1 rounded-lg dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-gray-850"
									on:click={() => {
										goto('/workspace/mcp');
									}}
									type="button"
								>
									<ChevronLeft strokeWidth="2.5" />
								</button>
							</Tooltip>
						</div>

						<div class="flex-1">
							<Tooltip content={$i18n.t('e.g. My MCP Server')} placement="top-start">
								<input
									class="w-full text-2xl font-medium bg-transparent outline-hidden font-primary"
									type="text"
									placeholder={$i18n.t('MCP Server Name')}
									bind:value={name}
									required
								/>
							</Tooltip>
						</div>

						<div class="self-center shrink-0">
							<button
								class="bg-gray-50 hover:bg-gray-100 text-black dark:bg-gray-850 dark:hover:bg-gray-800 dark:text-white transition px-2 py-1 rounded-full flex gap-1 items-center"
								type="button"
								on:click={() => {
									showAccessControlModal = true;
								}}
							>
								<LockClosed strokeWidth="2.5" className="size-3.5" />

								<div class="text-sm font-medium shrink-0">
									{$i18n.t('Access')}
								</div>
							</button>
						</div>
					</div>

					<div class=" flex gap-2 px-1 items-center">
						{#if edit}
							<div class="text-sm text-gray-500 shrink-0">
								{id}
							</div>
						{:else}
							<Tooltip className="w-full" content={$i18n.t('e.g. my_mcp_server')} placement="top-start">
								<input
									class="w-full text-sm disabled:text-gray-500 bg-transparent outline-hidden"
									type="text"
									placeholder={$i18n.t('MCP Server ID')}
									bind:value={id}
									required
									disabled={edit}
								/>
							</Tooltip>
						{/if}

						<Tooltip
							className="w-full self-center items-center flex"
							content={$i18n.t('e.g. MCP Server for performing various operations')}
							placement="top-start"
						>
							<input
								class="w-full text-sm bg-transparent outline-hidden"
								type="text"
								placeholder={$i18n.t('MCP Server Description')}
								bind:value={description}
								required
							/>
						</Tooltip>
					</div>
				</div>

        <!-- MCP Server Type: SSE or COMMAND -->
        <div class="flex flex-col gap-2">
          <div class="text-sm text-gray-500">
            {$i18n.t('MCP Server Type')}
          </div>
          <div class="flex flex-col gap-2">
            <!-- Select option for SSE or COMMAND -->
            <select class="w-full text-sm bg-transparent outline-hidden"
              bind:value={type}
              >
              <option value="sse">{$i18n.t('sse')}</option>
              <option value="command">{$i18n.t('command')}</option>
            </select>
          </div>
        </div>

        <!-- MCP Server Url -->
        <div class="flex flex-col gap-2"
          class:hidden={type !== 'sse'}
        >
          <div class="text-sm text-gray-500">
            {$i18n.t('MCP Server Url')}
          </div>
          <Tooltip
            className="w-full self-center items-center flex"
            content={$i18n.t('e.g. MCP Server for performing various operations')}
            placement="top-start"
            >
              <input
                class="w-full text-sm bg-transparent outline-hidden"
                type="text"
                placeholder={$i18n.t('MCP Server Url')}
                bind:value={url}
                required={type === 'command'}
              />
            </Tooltip>
        </div>

        <!-- MCP Server Command -->
        <div class="flex flex-col gap-2"
          class:hidden={type !== 'command'}
          >
          <div class="text-sm text-gray-500">
            {$i18n.t('MCP Server Command')}
          </div>
          <Tooltip
            className="w-full self-center items-center flex"
            content={$i18n.t('e.g. MCP Server for performing various operations')}
            placement="top-start"
            >
              <input
                class="w-full text-sm bg-transparent outline-hidden"
                type="text"
                placeholder={$i18n.t('MCP Server Command')}
                bind:value={command}
                required={type === 'command'}
              />
            </Tooltip>
        </div>

        <!-- MCP Server Valves -->
        <div class="flex flex-col gap-2">
          <div class="text-sm text-gray-500">
            {$i18n.t('MCP Server Valves')}
          </div>
          
        </div>

        <br>
				<div class="pb-3 flex justify-between">
					<!-- <div class="flex-1 pr-3">
						<div class="text-xs text-gray-500 line-clamp-2">
							<span class=" font-semibold dark:text-gray-200">{$i18n.t('Warning:')}</span>
							{$i18n.t('MCP Servers enhance the functionality of your LLM by allowing you to use custom tools')} <br />—
							<span class=" font-medium dark:text-gray-400"
								>{$i18n.t(`don't install random MCP Servers from sources you don't trust.`)}</span
							>
						</div>
					</div> -->

					<button
						class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"
						type="submit"
					>
						{$i18n.t('Save')}
					</button>
				</div>
			</div>
		</form>
	</div>
</div>

<ConfirmDialog
	bind:show={showConfirm}
	on:confirm={() => {
		saveHandler();
	}}
>
	<div class="text-sm text-gray-500">
		<div class=" bg-yellow-500/20 text-yellow-700 dark:text-yellow-200 rounded-lg px-4 py-3">
			<div>{$i18n.t('Please carefully review the following warnings:')}</div>

			<ul class=" mt-1 list-disc pl-4 text-xs">
				<li>
					{$i18n.t('MCP Servers enhance the functionality of your LLM by allowing you to use custom tools')}
				</li>
				<li>{$i18n.t('Do not install MCP Servers from sources you do not fully trust.')}</li>
			</ul>
		</div>

		<div class="my-3">
			{$i18n.t(
				'I acknowledge that I have read and I understand the implications of my action. I am aware of the risks associated with executing arbitrary code and I have verified the trustworthiness of the source.'
			)}
		</div>
	</div>
</ConfirmDialog>
