const apiUrl = 'http://localhost:5050';

async function fetchTodos() {
    const response = await fetch(`${apiUrl}/todos`);
    return await response.json();
}

async function fetchTags() {
    const response = await fetch(`${apiUrl}/todos/tags`);
    return await response.json();
}

function renderTags(tags) {
    const tagsList = document.getElementById('tags-list');
    tagsList.innerHTML = '';
    tags.forEach(tag => {
        const li = document.createElement('li');
        li.textContent = tag.name + ' (' + tag.count + ')';
        li.onclick = () => filterTodosByTag(tag.name);
        tagsList.appendChild(li);
    });
}

function filterTodosByTag(tag) {
    // Implement filtering logic here
}

async function init() {
    const todos = await fetchTodos();
    const tags = await fetchTags();
    renderTags(tags);
    // Render todos here
}

init();