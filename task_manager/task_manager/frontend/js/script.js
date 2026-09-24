

const API_URL = "/api/tasks";

const chainEl = document.getElementById("chain");
const emptyStateEl = document.getElementById("empty-state");
const formEl = document.getElementById("task-form");
const titleInput = document.getElementById("title-input");
const descriptionInput = document.getElementById("description-input");

async function loadTasks() {
  const response = await fetch(API_URL);
  const tasks = await response.json();
  renderChain(tasks);
}

function renderChain(tasks) {
  chainEl.innerHTML = "";
  emptyStateEl.hidden = tasks.length > 0;

  tasks.forEach((task, index) => {
    chainEl.appendChild(buildNodeElement(task, index === 0));

    if (index < tasks.length - 1) {
      chainEl.appendChild(buildConnectorElement());
    }
  });

  if (tasks.length > 0) {
    chainEl.appendChild(buildTerminatorElement());
  }
}

function buildNodeElement(task, isHead) {
  const node = document.createElement("article");
  node.className = "node" + (isHead ? " node--head" : "") + (task.completed ? " node--done" : "");

  node.innerHTML = `
    <div class="node__row">
      <span class="node__id">nodo #${task.id}</span>
      ${isHead ? '<span class="node__label">HEAD</span>' : ""}
    </div>
    <p class="node__title">${escapeHtml(task.title)}</p>
    <p class="node__desc">${escapeHtml(task.description || "")}</p>
    <div class="node__actions">
      <button class="btn-toggle" data-action="toggle" data-id="${task.id}">
        ${task.completed ? "Reabrir" : "Completar"}
      </button>
      <button class="btn-delete" data-action="delete" data-id="${task.id}">Eliminar</button>
    </div>
    <div class="node__pointer">next &rarr; ${task.next !== null ? "nodo #" + task.next : "NULL"}</div>
  `;

  return node;
}

function buildConnectorElement() {
  const connector = document.createElement("div");
  connector.className = "connector";
  return connector;
}

function buildTerminatorElement() {
  const terminator = document.createElement("div");
  terminator.className = "terminator";
  terminator.textContent = "NULL";
  return terminator;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

formEl.addEventListener("submit", async (event) => {
  event.preventDefault();

  const title = titleInput.value.trim();
  const description = descriptionInput.value.trim();
  if (!title) return;

  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description }),
  });

  titleInput.value = "";
  descriptionInput.value = "";
  await loadTasks();
});

chainEl.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const taskId = button.dataset.id;
  const action = button.dataset.action;

  if (action === "toggle") {
    await fetch(`${API_URL}/${taskId}`, { method: "PATCH" });
  } else if (action === "delete") {
    await fetch(`${API_URL}/${taskId}`, { method: "DELETE" });
  }

  await loadTasks();
});

loadTasks();
