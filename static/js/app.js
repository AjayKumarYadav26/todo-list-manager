const API_BASE = '/api';

const els = {
  todoItems: document.getElementById('todo-items'),
  emptyState: document.getElementById('empty-state'),
  todoCount: document.getElementById('todo-count'),
  searchInput: document.getElementById('search-input'),
  filterStatus: document.getElementById('filter-status'),
  filterPriority: document.getElementById('filter-priority'),
  filterCategory: document.getElementById('filter-category'),
  sortBy: document.getElementById('sort-by'),
  sortOrderBtn: document.getElementById('sort-order-btn'),
  form: document.getElementById('todo-form-el'),
  title: document.getElementById('input-title'),
  description: document.getElementById('input-description'),
  priority: document.getElementById('input-priority'),
  category: document.getElementById('input-category'),
  dueDate: document.getElementById('input-due-date'),
  editModal: document.getElementById('edit-modal'),
  editForm: document.getElementById('edit-form-el'),
  editId: document.getElementById('edit-id'),
  editTitle: document.getElementById('edit-title'),
  editDescription: document.getElementById('edit-description'),
  editStatus: document.getElementById('edit-status'),
  editPriority: document.getElementById('edit-priority'),
  editCategory: document.getElementById('edit-category'),
  editDueDate: document.getElementById('edit-due-date'),
};

let todos = [];
let sortOrder = 'desc';

function formatTimestamp(value) {
  if (!value) return 'Created: Unknown';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return `Created: ${value}`;
  return `Created: ${date.toLocaleString()}`;
}

function escapeHtml(str) {
  return String(str || '').replace(/[&<>"]+/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[s]));
}

function renderTodo(todo) {
  return `
    <article class="todo-card" data-id="${todo.id}">
      <div class="todo-card__header">
        <h3>${escapeHtml(todo.title)}</h3>
        <span class="todo-badge todo-status ${todo.status}">${todo.status.replace('_', ' ')}</span>
      </div>
      <p class="todo-description">${escapeHtml(todo.description || '')}</p>
      <div class="todo-meta">
        <span class="todo-meta__item">Priority: ${escapeHtml(todo.priority)}</span>
        ${todo.category ? `<span class="todo-meta__item">Category: ${escapeHtml(todo.category)}</span>` : ''}
        ${todo.due_date ? `<span class="todo-meta__item">Due: ${escapeHtml(todo.due_date)}</span>` : ''}
        <span class="todo-meta__item todo-created-at">${escapeHtml(formatTimestamp(todo.created_at))}</span>
      </div>
    </article>`;
}

async function loadTodos() {
  const params = new URLSearchParams();
  if (els.searchInput.value) params.set('search', els.searchInput.value);
  if (els.filterStatus.value) params.set('status', els.filterStatus.value);
  if (els.filterPriority.value) params.set('priority', els.filterPriority.value);
  if (els.filterCategory.value) params.set('category', els.filterCategory.value);
  params.set('sort_by', els.sortBy.value);
  params.set('sort_order', sortOrder);
  const res = await fetch(`${API_BASE}/todos?${params.toString()}`);
  todos = await res.json();
  renderTodos();
}

function renderTodos() {
  els.todoItems.innerHTML = todos.map(renderTodo).join('');
  els.emptyState.style.display = todos.length ? 'none' : 'block';
  els.todoCount.textContent = `${todos.length} todo${todos.length === 1 ? '' : 's'}`;
}

async function init() {
  await loadTodos();
}

init();
