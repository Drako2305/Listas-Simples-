
class TaskNode:
    """A single node of the pending-tasks linked list."""

    _next_id = 1  

    def __init__(self, title: str, description: str = ""):
        self.id = TaskNode._next_id
        TaskNode._next_id += 1

        self.title = title
        self.description = description
        self.completed = False

     
        self.next = None

    def to_dict(self) -> dict:
        """Serializes the node so it can be sent to the frontend as JSON.

        `next` is exposed as the id of the following node (or None),
        never as the object itself, since a live object reference
        cannot be turned into JSON.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "next": self.next.id if self.next is not None else None,
        }

    def __repr__(self):
        return f"TaskNode(id={self.id}, title={self.title!r}, next={self.next.id if self.next else None})"
