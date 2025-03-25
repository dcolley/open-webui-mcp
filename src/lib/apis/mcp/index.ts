import { WEBUI_API_BASE_URL } from '$lib/constants';

export const createNewMCPServer = async (token: string, mcp_server: object) => {
	console.log('createNewMCPServer', mcp_server);
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/create`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			...mcp_server
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getMCPServers = async (token: string = '') => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getMCPServerById = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/${id}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

// export const exportMCP_Servers = async (token: string = '') => {
// 	let error = null;

// 	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/export`, {
// 		method: 'GET',
// 		headers: {
// 			Accept: 'application/json',
// 			'Content-Type': 'application/json',
// 			authorization: `Bearer ${token}`
// 		}
// 	})
// 		.then(async (res) => {
// 			if (!res.ok) throw await res.json();
// 			return res.json();
// 		})
// 		.then((json) => {
// 			return json;
// 		})
// 		.catch((err) => {
// 			error = err.detail;
// 			console.log(err);
// 			return null;
// 		});
// 	if (error) {
// 		throw error;
// 	}
// 	return res;
// };

// export const getMCP_ServerById = async (token: string, id: string) => {
// 	let error = null;
// 	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/${id}`, {
// 		method: 'GET',
// 		headers: {
// 			Accept: 'application/json',
// 			'Content-Type': 'application/json',
// 			authorization: `Bearer ${token}`
// 		}
// 	})
// 		.then(async (res) => {
// 			if (!res.ok) throw await res.json();
// 			return res.json();
// 		})
// 		.then((json) => {
// 			return json;
// 		})
// 		.catch((err) => {
// 			error = err.detail;
// 			console.log(err);
// 			return null;
// 		});
// 	if (error) {
// 		throw error;
// 	}
// 	return res;
// };

export const updateMCPServerById = async (token: string, id: string, mcp_server: object) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/${id}/edit`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			...mcp_server
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const deleteMCPServerById = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/${id}/delete`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getMCPServerValvesById = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/${id}/valves`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

// export const getMCPServerValvesSpecById = async (token: string, id: string) => {
// 	let error = null;

// 	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/${id}/valves/spec`, {
// 		method: 'GET',
// 		headers: {
// 			Accept: 'application/json',
// 			'Content-Type': 'application/json',
// 			authorization: `Bearer ${token}`
// 		}
// 	})
// 		.then(async (res) => {
// 			if (!res.ok) throw await res.json();
// 			return res.json();
// 		})
// 		.then((json) => {
// 			return json;
// 		})
// 		.catch((err) => {
// 			error = err.detail;

// 			console.log(err);
// 			return null;
// 		});

// 	if (error) {
// 		throw error;
// 	}

// 	return res;
// };

export const updateMCPServerValvesById = async (token: string, id: string, valves: object) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/mcp/${id}/valves`, {
		method: 'PUT',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			...valves
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

// export const getUserMCP_ServerValvesById = async (token: string, id: string) => {
// 	let error = null;

// 	const res = await fetch(`${WEBUI_API_BASE_URL}/tools/id/${id}/valves/user`, {
// 		method: 'GET',
// 		headers: {
// 			Accept: 'application/json',
// 			'Content-Type': 'application/json',
// 			authorization: `Bearer ${token}`
// 		}
// 	})
// 		.then(async (res) => {
// 			if (!res.ok) throw await res.json();
// 			return res.json();
// 		})
// 		.then((json) => {
// 			return json;
// 		})
// 		.catch((err) => {
// 			error = err.detail;

// 			console.log(err);
// 			return null;
// 		});

// 	if (error) {
// 		throw error;
// 	}

// 	return res;
// };

export const getUserValvesSpecById = async (token: string, id: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/tools/id/${id}/valves/user/spec`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const updateUserValvesById = async (token: string, id: string, valves: object) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/tools/id/${id}/valves/user/update`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			...valves
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};
