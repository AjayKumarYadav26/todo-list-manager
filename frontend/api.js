const API_BASE = '/api';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.status === 204 ? null : response.json();
}

async function getTodos() {
  return request('/todos');
}

async function createTodo(title) {
  return request('/todos', {
    method: 'POST',
    body: JSON.stringify({ title }),
  });
}
