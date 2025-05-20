from typing import List, Union
from sqlalchemy import select
from models import Session, Todo
from crewai.tools import tool


@tool("Get All Todos")
def getAllTodos(_=None) -> str:
    """Get all todos from the database. Returns a list of todos with their IDs."""
    with Session() as session:
        todos = session.execute(select(Todo)).scalars().all()
        return str([{"id": todo.id, "todo": todo.todo} for todo in todos])


@tool("Create Todo")
def createTodo(todo_text: str) -> str:
    """Create a new todo in the database. Returns the ID of the created todo."""
    if not isinstance(todo_text, str):
        raise ValueError("Todo text must be a string")
    with Session() as session:
        new_todo = Todo(todo=todo_text)
        session.add(new_todo)
        session.commit()
        return f"Created todo with ID: {new_todo.id}"


@tool("Delete Todo")
def deleteTodoById(todo_id: Union[int, str]) -> str:
    """Delete a todo by its ID. Returns a confirmation message."""
    if todo_id is None:
        raise ValueError("Todo ID cannot be None")

    try:
        todo_id = int(todo_id)
    except (ValueError, TypeError):
        raise ValueError("Todo ID must be a number")

    with Session() as session:
        todo = session.get(Todo, todo_id)
        if todo:
            session.delete(todo)
            session.commit()
            return f"Deleted todo with ID: {todo_id}"
        return f"No todo found with ID: {todo_id}"


@tool("Search Todos")
def searchTodo(search_text: str) -> str:
    """Search for todos containing specific text. Returns matching todos."""
    if not search_text:
        raise ValueError("Search text cannot be empty")

    with Session() as session:
        todos = (
            session.execute(select(Todo).where(Todo.todo.ilike(f"%{search_text}%")))
            .scalars()
            .all()
        )
        return str([{"id": todo.id, "todo": todo.todo} for todo in todos])
