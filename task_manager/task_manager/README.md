# Task List &mdash; Singly Linked List (Python + Flask)

A pending-tasks manager where each task is a **node** with a reference
(`next`) to the following node in the list — the same pattern used in
class for `Contact` / `ContactList`, applied to a to-do list, with a
web frontend that draws the chain of nodes and their pointers.

## Folder structure

```
task_manager/
├── backend/
│   ├── app.py                # Flask app: REST API + serves the frontend
│   ├── requirements.txt
│   └── models/
│       ├── __init__.py
│       ├── task_node.py      # TaskNode: data + `next` pointer
│       └── task_list.py      # TaskList: the linked list (add/find/toggle/delete/traverse)
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js         # fetches /api/tasks and renders the node chain
└── README.md
```

## How to run it

```bash
cd task_manager/backend
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser. Flask serves both
the API and the frontend, so this single command is all you need.

## API

| Method | Route                | Body                          | Description                  |
|--------|-----------------------|--------------------------------|-------------------------------|
| GET    | `/api/tasks`          | —                              | List every node, in order     |
| POST   | `/api/tasks`          | `{ "title", "description" }`   | Append a new node             |
| PATCH  | `/api/tasks/<id>`     | —                               | Toggle a task's `completed`   |
| DELETE | `/api/tasks/<id>`     | —                               | Remove a node, relink chain   |

## How the linked list works

- `TaskList` only stores `first_node` (the head) and `last_node` (the tail).
- Adding a task links it after `last_node` — O(1).
- Finding, toggling, listing, and printing all traverse the chain from
  `first_node`, following `.next` until it hits `None`.
- Deleting a node keeps a `previous_node` pointer while walking the
  list, so it can reconnect `previous_node.next` to the node that
  came after the one removed.
- The frontend never invents this order — `GET /api/tasks` returns the
  nodes already walked in list order, and the UI draws an arrow
  between each pair, ending in `NULL`, mirroring the diagrams from
  the slides.
