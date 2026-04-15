const API_BASE = '/api';

const state = {
  todos: [],
  filters: {
    status: '',
    priority: '',
    category: '',
    search: '',
  },
};

const els = {};

document.addEventListener('DOMContentLoaded', () => {
  cacheElements();
  bindEvents();
  loadTodos();
});

function cacheElements() {
  els.todoList = document.getElementById('todo-list');
  els.todoForm = document.getElementById('todo-form');
  els.titleInput = document.getElementById('title');
  els.descriptionInput = document.getElementById('description');
  els.priorityInput = document.getElementById('priority');
  els.categoryInput = document.getElementById('category');
  els.dueDateInput = document.getElementById('due_date');
  els.searchInput = document.getElementById('search');
  els.statusFilter = document.getElementById('filter-status');
  els.priorityFilter = document.getElementById('filter-priority');
  els.categoryFilter = document.getElementById('filter-category');
  els.clearFiltersBtn = document.getElementById('clear-filters');
}

function bindEvents() {
  els.todoForm?.addEventListener('submit', handleCreateTodo);
  els.searchInput?.addEventListener('input', debounce(() => {
    state.filters.search = els.searchInput.value.trim();
    loadTodos();
  }, 250));
  els.statusFilter?.addEventListener('change', () => {
    state.filters.status = els.statusFilter.value;
    loadTodos();
  });
  els.priorityFilter?.addEventListener('change', () => {
    state.filters.priority = els.priorityFilter.value;
    loadTodos();
  });
  els.categoryFilter?.addEventListener('change', () => {
    state.filters.category = els.categoryFilter.value;
    loadTodos();
  });
  els.clearFiltersBtn?.addEventListener('click', () => {
    state.filters = { status: '', priority: '', category: '', search: '' };
    if (els.todoForm) els.todoForm.reset();
    if (els.searchInput) els.searchInput.value = '';
    if (els.statusFilter) els.statusFilter.value = '';
    if (els.priorityFilter) els.priorityFilter.value = '';
    if (els.categoryFilter) els.categoryFilter.value = '';
    loadTodos();
  });
}

async function loadTodos() {
  const params = new URLSearchParams();
  Object.entries(state.filters).forEach(([key, value]) => {
    if (value) params.set(key, value);
  });

  const res = await fetch(`${API_BASE}/todos?${params.toString()}`);
  state.todos = await res.json();
  renderTodos();
}

function renderTodos() {
  if (!els.todoList) return;
  if (!state.todos.length) {
    els.todoList.innerHTML = '<div class="empty-state">No todos found.</div>';
    return;
  }

  els.todoList.innerHTML = state.todos.map(renderTodoCard).join('');
}

function renderTodoCard(todo) {
  const createdAt = formatCreatedAt(todo.created_at);
  return `
    <article class="todo-card">
      <div class="todo-card__header">
        <h3 class="todo-card__title">${escapeHtml(todo.title || '')}</h3>
        <span class="todo-card__status todo-card__status--${escapeHtml(todo.status || 'pending')}">${escapeHtml(todo.status || 'pending')}</span>
      </div>
      <p class="todo-card__meta">Created: ${createdAt}</p>
      ${todo.description ? `<p class="todo-card__description">${escapeHtml(todo.description)}</p>` : ''}
    </article>
  `;
}

function formatCreatedAt(createdAt) {
  if (!createdAt) return 'Unknown';
  const date = new Date(createdAt);
  if (Number.isNaN(date.getTime())) return 'Unknown';
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date);
}

async function handleCreateTodo(event) {
  event.preventDefault();
  const payload = {
    title: els.titleInput.value,
    description: els.descriptionInput.value,
    priority: els.priorityInput.value,
    category: els.categoryInput.value,
    due_date: els.dueDateInput.value,
  };

  await fetch(`${API_BASE}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  els.todoForm.reset();
  loadTodos();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}
