// ===== State =====
let todos = [];
let categories = [];
let stats = {};
let sortOrder = "desc";

// ===== DOM Elements =====
const $ = (sel) => document.querySelector(sel);
const todoItems = $("#todo-items");
const emptyState = $("#empty-state");
const todoCount = $("#todo-count");
const searchInput = $("#search-input");
const filterStatus = $("#filter-status");
const filterPriority = $("#filter-priority");
const filterCategory = $("#filter-category");
const sortBy = $("#sort-by");
const sortOrderBtn = $("#sort-order-btn");
const clearCompletedBtn = $("#clear-completed-btn");
const todoFormEl = $("#todo-form-el");
const editModal = $("#edit-modal");
const editFormEl = $("#edit-form-el");
const statsToggle = $("#stats-toggle");
const statsContent = $("#stats-content");
const themeToggle = $("#theme-toggle");

// ===== Init =====
document.addEventListener("DOMContentLoaded", init);

function init() {
    loadTheme();
    fetchCategories();
    fetchTodos();
    fetchStats();
    bindEvents();
}

function bindEvents() {
    todoFormEl.addEventListener("submit", handleAddTodo);
    editFormEl.addEventListener("submit", handleEditSave);
    searchInput.addEventListener("input", debounce(fetchTodos, 300));
    filterStatus.addEventListener("change", fetchTodos);
    filterPriority.addEventListener("change", fetchTodos);
    filterCategory.addEventListener("change", fetchTodos);
    sortBy.addEventListener("change", fetchTodos);
    sortOrderBtn.addEventListener("click", () => {
        sortOrder = sortOrder === "desc" ? "asc" : "desc";
        sortOrderBtn.textContent = sortOrder === "desc" ? "\u2195" : "\u2195";
        sortOrderBtn.title = `Sort: ${sortOrder === "desc" ? "Descending" : "Ascending"}`;
        fetchTodos();
    });
    clearCompletedBtn.addEventListener("click", handleClearCompleted);
    statsToggle.addEventListener("click", () => {
        statsContent.classList.toggle("collapsed");
        const arrow = statsToggle.querySelector(".toggle-arrow");
        arrow.style.transform = statsContent.classList.contains("collapsed") ? "rotate(-90deg)" : "";
    });
    themeToggle.addEventListener("click", toggleTheme);
    editModal.addEventListener("click", (e) => {
        if (e.target === editModal || e.target.classList.contains("modal-close")) {
            editModal.style.display = "none";
        }
    });
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && editModal.style.display !== "none") {
            editModal.style.display = "none";
        }
    });
}

// ===== API Calls =====
async function fetchTodos() {
    const params = new URLSearchParams();
    if (searchInput.value) params.set("search", searchInput.value);
    if (filterStatus.value) params.set("status", filterStatus.value);
    if (filterPriority.value) params.set("priority", filterPriority.value);
    if (filterCategory.value) params.set("category", filterCategory.value);
    params.set("sort_by", sortBy.value);
    params.set("sort_order", sortOrder);

    try {
        const res = await fetch(`/api/todos?${params}`);
        todos = await res.json();
        renderTodoList();
    } catch (err) {
        showToast("Failed to load todos", "error");
    }
}

async function fetchCategories() {
    try {
        const res = await fetch("/api/categories");
        categories = await res.json();
        renderCategories();
    } catch (err) {
        // silent
    }
}

async function fetchStats() {
    try {
        const res = await fetch("/api/stats");
        stats = await res.json();
        renderStats();
    } catch (err) {
        // silent
    }
}

// ===== Handlers =====
async function handleAddTodo(e) {
    e.preventDefault();
    const data = {
        title: $("#input-title").value,
        description: $("#input-description").value,
        priority: $("#input-priority").value,
        category: $("#input-category").value,
        due_date: $("#input-due-date").value || null,
    };

    try {
        const res = await fetch("/api/todos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) {
            const err = await res.json();
            showToast(err.error || "Failed to create todo", "error");
            return;
        }
        todoFormEl.reset();
        showToast("Todo added!", "success");
        fetchTodos();
        fetchStats();
        fetchCategories();
    } catch (err) {
        showToast("Network error", "error");
    }
}

async function handleEditSave(e) {
    e.preventDefault();
    const id = $("#edit-id").value;
    const data = {
        title: $("#edit-title").value,
        description: $("#edit-description").value,
        status: $("#edit-status").value,
        priority: $("#edit-priority").value,
        category: $("#edit-category").value,
        due_date: $("#edit-due-date").value || null,
    };

    try {
        const res = await fetch(`/api/todos/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) {
            const err = await res.json();
            showToast(err.error || "Failed to update", "error");
            return;
        }
        editModal.style.display = "none";
        showToast("Todo updated!", "success");
        fetchTodos();
        fetchStats();
        fetchCategories();
    } catch (err) {
        showToast("Network error", "error");
    }
}

async function handleStatusChange(id, newStatus) {
    try {
        const res = await fetch(`/api/todos/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus }),
        });
        if (res.ok) {
            fetchTodos();
            fetchStats();
        }
    } catch (err) {
        showToast("Failed to update status", "error");
    }
}

async function handleDelete(id) {
    if (!confirm("Delete this todo?")) return;
    try {
        const res = await fetch(`/api/todos/${id}`, { method: "DELETE" });
        if (res.ok) {
            showToast("Todo deleted", "info");
            fetchTodos();
            fetchStats();
        }
    } catch (err) {
        showToast("Failed to delete", "error");
    }
}

async function handleClearCompleted() {
    if (!confirm("Delete all completed todos?")) return;
    try {
        const res = await fetch("/api/todos?completed=true", { method: "DELETE" });
        const data = await res.json();
        if (res.ok) {
            showToast(`Cleared ${data.count} completed todo(s)`, "info");
            fetchTodos();
            fetchStats();
        }
    } catch (err) {
        showToast("Failed to clear", "error");
    }
}

function openEditModal(todo) {
    $("#edit-id").value = todo.id;
    $("#edit-title").value = todo.title;
    $("#edit-description").value = todo.description || "";
    $("#edit-status").value = todo.status;
    $("#edit-priority").value = todo.priority;
    $("#edit-category").value = todo.category || "";
    $("#edit-due-date").value = todo.due_date || "";
    editModal.style.display = "flex";
    $("#edit-title").focus();
}

// ===== Rendering =====
function renderTodoList() {
    if (todos.length === 0) {
        todoItems.innerHTML = "";
        emptyState.style.display = "block";
        todoCount.textContent = "0 todos";
        return;
    }

    emptyState.style.display = "none";
    todoCount.textContent = `${todos.length} todo${todos.length !== 1 ? "s" : ""}`;
    todoItems.innerHTML = todos.map(renderTodoCard).join("");
}

function renderTodoCard(todo) {
    const isCompleted = todo.status === "completed";
    const dueBadge = getDueBadge(todo);
    const createdAtBadge = getCreatedAtBadge(todo);
    const statusLabel = {
        pending: "Pending",
        in_progress: "In Progress",
        completed: "Completed",
    };

    return `
    <div class="todo-card priority-${todo.priority} status-${todo.status}">
        <div class="todo-checkbox">
            <input type="checkbox"
                   ${isCompleted ? "checked" : ""}
                   onchange="handleStatusChange('${todo.id}', this.checked ? 'completed' : 'pending')"
                   title="Mark as ${isCompleted ? 'pending' : 'completed'}">
        </div>
        <div class="todo-body">
            <div class="todo-title">${escapeHtml(todo.title)}</div>
            ${todo.description ? `<div class="todo-description">${escapeHtml(todo.description)}</div>` : ""}
            <div class="todo-meta">
                <span class="badge badge-status ${todo.status}">${statusLabel[todo.status]}</span>
                <span class="badge badge-priority ${todo.priority}">${capitalize(todo.priority)}</span>
                ${todo.category ? `<span class="badge badge-category">${escapeHtml(todo.category)}</span>` : ""}
                ${dueBadge}
            </div>
            ${createdAtBadge}
            ${!isCompleted ? `
            <div class="status-btn-group" style="margin-top:0.5rem;">
                <button class="status-btn ${todo.status === 'pending' ? 'active' : ''}"
                        onclick="handleStatusChange('${todo.id}', 'pending')">Pending</button>
                <button class="status-btn ${todo.status === 'in_progress' ? 'active' : ''}"
                        onclick="handleStatusChange('${todo.id}', 'in_progress')">In Progress</button>
                <button class="status-btn ${todo.status === 'completed' ? 'active' : ''}"
                        onclick="handleStatusChange('${todo.id}', 'completed')">Done</button>
            </div>` : ""}
        </div>
        <div class="todo-actions">
            <button onclick='openEditModal(${JSON.stringify(todo).replace(/'/g, "&#39;")})' title="Edit">&#9998;</button>
            <button class="btn-delete" onclick="handleDelete('${todo.id}')" title="Delete">&#10005;</button>
        </div>
    </div>`;
}

function getDueBadge(todo) {
    if (!todo.due_date) return "";
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const due = new Date(todo.due_date + "T00:00:00");
    const diffDays = Math.round((due - today) / (1000 * 60 * 60 * 24));

    if (todo.status === "completed") {
        return `<span class="badge badge-due">${todo.due_date}</span>`;
    }

    if (diffDays < 0) {
        return `<span class="badge badge-due overdue">Overdue by ${Math.abs(diffDays)} day${Math.abs(diffDays) !== 1 ? "s" : ""}</span>`;
    } else if (diffDays === 0) {
        return `<span class="badge badge-due overdue">Due today</span>`;
    } else if (diffDays <= 3) {
        return `<span class="badge badge-due" style="color:var(--warning)">Due in ${diffDays} day${diffDays !== 1 ? "s" : ""}</span>`;
    }
    return `<span class="badge badge-due">${todo.due_date}</span>`;
}

function getCreatedAtBadge(todo) {
    if (!todo.created_at) return "";
    return `<div class="todo-created-at">Created on: ${formatCreatedAt(todo.created_at)}</div>`;
}

function formatCreatedAt(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return escapeHtml(value);
    return new Intl.DateTimeFormat(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
    }).format(date);
}

function renderStats() {
    $("#stat-total").textContent = stats.total || 0;
    $("#stat-pending").textContent = stats.by_status?.pending || 0;
    $("#stat-in-progress").textContent = stats.by_status?.in_progress || 0;
    $("#stat-completed").textContent = stats.by_status?.completed || 0;
    $("#stat-overdue").textContent = stats.overdue_count || 0;
    $("#stat-rate").textContent = `${stats.completion_rate || 0}%`;
}

function renderCategories() {
    const datalist = $("#category-list");
    datalist.innerHTML = categories.map((c) => `<option value="${escapeHtml(c)}">`).join("");

    const select = filterCategory;
    const current = select.value;
    select.innerHTML = '<option value="">All Categories</option>' +
        categories.map((c) => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join("");
    select.value = current;
}

// ===== Theme =====
function loadTheme() {
    const saved = localStorage.getItem("todo-theme") || "light";
    document.body.setAttribute("data-theme", saved);
    updateThemeIcon(saved);
}

function toggleTheme() {
    const current = document.body.getAttribute("data-theme");
    const next = current === "light" ? "dark" : "light";
    document.body.setAttribute("data-theme", next);
    localStorage.setItem("todo-theme", next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector(".theme-icon");
    icon.textContent = theme === "light" ? "\u263D" : "\u2600";
}

// ===== Toast =====
function showToast(message, type = "info") {
    const container = $("#toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// ===== Utilities =====
function debounce(fn, ms) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), ms);
    };
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
