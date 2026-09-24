"""
app.py

Small Flask API that sits on top of the TaskList (singly linked list).
It also serves the static frontend, so running this one file gives you
the whole app at http://127.0.0.1:5000

Endpoints
---------
GET    /api/tasks              -> list every task, in list order
POST   /api/tasks               -> add a new task   {title, description}
PATCH  /api/tasks/<task_id>     -> toggle completed
DELETE /api/tasks/<task_id>     -> remove a task
"""

import os
from flask import Flask, jsonify, request, send_from_directory

from models import TaskList

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

# A single, in-memory linked list shared by every request.
task_list = TaskList()

# Some starter data so the visualization isn't empty on first run.
task_list.add_task("Study linked lists", "Review nodes and pointers")
task_list.add_task("Build the API", "Flask endpoints for the task list")
task_list.add_task("Connect the frontend", "Fetch and render the nodes")


# ---------------------------------------------------------------------- #
# Frontend
# ---------------------------------------------------------------------- #
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


# ---------------------------------------------------------------------- #
# API
# ---------------------------------------------------------------------- #
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(task_list.to_list())


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()

    if not title:
        return jsonify({"error": "title is required"}), 400

    new_node = task_list.add_task(title, description)
    return jsonify(new_node.to_dict()), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def toggle_task(task_id):
    node = task_list.toggle_task(task_id)
    if node is None:
        return jsonify({"error": "task not found"}), 404
    return jsonify(node.to_dict())


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = task_list.delete_task(task_id)
    if not deleted:
        return jsonify({"error": "task not found"}), 404
    return jsonify({"deleted": task_id})


if __name__ == "__main__":
    app.run(debug=True)
