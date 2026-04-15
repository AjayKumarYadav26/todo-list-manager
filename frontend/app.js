async function init() {
  const form = document.getElementById('todo-form');
  const input = document.getElementById('todo-title');

  async function loadTodos() {
    const todos = await getTodos();
    renderTodos(todos);
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const title = input.value.trim();
    if (!title) return;
    await createTodo(title);
    input.value = '';
    await loadTodos();
  });

  await loadTodos();
}

document.addEventListener('DOMContentLoaded', () => {
  init().catch((error) => {
    console.error(error);
    const list = document.getElementById('todo-list');
    list.innerHTML = '<p class="error">Failed to load todos.</p>';
  });
});
