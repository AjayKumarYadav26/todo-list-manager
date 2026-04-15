const API_BASE = '/api';

function formatCreatedAt(value) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderTodoCard(todo) {
  const createdAt = formatCreatedAt(todo.created_at);
  return `
    <article class="todo-card" data-id="${escapeHtml(todo.id)}">
      <div class="todo-card__header">
        <h3 class="todo-card__title">${escapeHtml(todo.title || 'Untitled todo')}</h3>
      </div>
      ${todo.description ? `<p class="todo-card__description">${escapeHtml(todo.description)}</p>` : ''}
      <div class="todo-card__meta">
        ${createdAt ? `<span class="todo-card__timestamp">Created ${escapeHtml(createdAt)}</span>` : ''}
      </div>
    </article>
  `;
}

async function fetchTodos() {
  const response = await fetch(`${API_BASE}/todos`);
  if (!response.ok) throw new Error('Failed to load todos');
  return response.json();
}

function renderTodos(todos) {
  const container = document.getElementById('todo-list');
  if (!container) return;
  container.innerHTML = todos.map(renderTodoCard).join('');
}

async function init() {
  try {
    const todos = await fetchTodos();
    renderTodos(Array.isArray(todos) ? todos : todos.items || []);
  } catch (error) {
    const container = document.getElementById('todo-list');
    if (container) container.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
  }
}

document.addEventListener('DOMContentLoaded', init);
