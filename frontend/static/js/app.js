const todos = [];
const popularTags = {};

function renderTodos() {
    const container = document.getElementById('todos-container');
    container.innerHTML = '';
    todos.forEach(todo => {
        const todoCard = document.createElement('div');
        todoCard.className = 'todo-card';
        todoCard.innerHTML = `<h3>${todo.title}</h3><p>${todo.description}</p>`;
        todo.tags.forEach(tag => {
            const tagBadge = document.createElement('span');
            tagBadge.className = 'tag-badge';
            tagBadge.innerText = tag;
            todoCard.appendChild(tagBadge);
        });
        container.appendChild(todoCard);
    });
}

function addTagToTodo(id, tag) {
    const todo = todos.find(t => t.id === id);
    if (todo) {
        todo.tags.push(tag);
        renderTodos();
        updatePopularTags(tag);
    }
}

function updatePopularTags(tag) {
    popularTags[tag] = (popularTags[tag] || 0) + 1;
    renderPopularTags();
}

function renderPopularTags() {
    const container = document.getElementById('popular-tags-container');
    container.innerHTML = '<h2>Popular Tags</h2>';
    for (const tag in popularTags) {
        const tagElement = document.createElement('div');
        tagElement.innerText = `${tag}: ${popularTags[tag]}`;
        container.appendChild(tagElement);
    }
}