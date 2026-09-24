

from .task_node import TaskNode


class TaskList:
    """Singly linked list that stores pending tasks."""

    def __init__(self):
        self.first_node = None
        self.last_node = None


    def add_task(self, title: str, description: str = "") -> TaskNode:
        """Creates a new node and appends it at the end of the list."""
        new_node = TaskNode(title, description)

        if self.first_node is None:
       
            self.first_node = new_node
            self.last_node = new_node
        else:
            self.last_node.next = new_node
            self.last_node = new_node

        return new_node

   
    def find_task(self, task_id: int) -> TaskNode | None:
        """Traverses the list looking for the node with the given id."""
        current_node = self.first_node
        while current_node is not None:
            if current_node.id == task_id:
                return current_node
            current_node = current_node.next
        return None

   
    def toggle_task(self, task_id: int) -> TaskNode | None:
        """Flips the completed state of a task, returns the node or None."""
        node = self.find_task(task_id)
        if node is not None:
            node.completed = not node.completed
        return node

  
    def delete_task(self, task_id: int) -> bool:
        """Removes the node with the given id, reconnecting its neighbors.

        Returns True if a node was removed, False if no task had that id.
        """
        previous_node = None
        current_node = self.first_node

        while current_node is not None:
            if current_node.id == task_id:
                if previous_node is None:
                    # Removing the head of the list
                    self.first_node = current_node.next
                else:
                    previous_node.next = current_node.next

                if current_node is self.last_node:
                    self.last_node = previous_node

                return True

            previous_node = current_node
            current_node = current_node.next

        return False

    def to_list(self) -> list[dict]:
        """Walks the chain and returns every node as a plain dict.

        This is what gets sent to the frontend so it can draw the
        nodes in order, following each `next` pointer.
        """
        tasks = []
        current_node = self.first_node
        while current_node is not None:
            tasks.append(current_node.to_dict())
            current_node = current_node.next
        return tasks

    def print_tasks(self) -> None:
        """Console version of print_contacts() from the class example."""
        if self.first_node is None:
            print("Task list is empty")
            return

        current_node = self.first_node
        while current_node is not None:
            print("Id:", current_node.id)
            print("Title:", current_node.title)
            print("Completed:", current_node.completed)
            print("Next:", current_node.next.id if current_node.next else None)
            print("-" * 40)
            current_node = current_node.next
