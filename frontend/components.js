function formatCreatedAt(createdAt) {
  if (!createdAt) return 'Created: Unknown';
  const date = new Date(createdAt);
  if (Number.isNaN(date.getTime())) return `Created: ${createdAt}`;
  return `Created: ${date.toLocaleString()}`;
}

function todoCard(todo) {
  const card = document.createElement('article');
  card.className = 'todo-card';

  const title = document.createElement('h2');
  title.textContent = todo.title;

  const timestamp = document.createElement('p');
  timestamp.className = 'todo-timestamp';
  timestamp.textContent = formatCreatedAt(todo.created_at);

  card.append(title, timestamp);
  return card;
}

function renderTodos(todos) {
  const list = document.getElementById('todo-list');
  list.innerHTML = '';
  todos.forEach((todo) => list.appendChild(todoCard(todo)));
}
