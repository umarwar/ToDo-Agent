from typing import List, Union
from sqlalchemy import select
from models import Session, Todo


def get_all_todos(_=None) -> list[dict]:
    with Session() as session:
        todos = session.execute(select(Todo)).scalars().all()
        return [{"id": todo.id, "todo": todo.todo} for todo in todos]


def create_todo(todo_text: str) -> int:
    if not isinstance(todo_text, str):
        raise ValueError("Todo text must be a string")
    with Session() as session:
        new_todo = Todo(todo=todo_text)
        session.add(new_todo)
        session.commit()
        return new_todo.id


def delete_todo_by_id(todo_id: Union[int, str]) -> None:
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


def search_todo(search_text: str) -> List[dict]:
    if not search_text:
        raise ValueError("Search text cannot be empty")

    with Session() as session:
        todos = (
            session.execute(select(Todo).where(Todo.todo.ilike(f"%{search_text}%")))
            .scalars()
            .all()
        )
        return [{"id": todo.id, "todo": todo.todo} for todo in todos]


tools = {
    "getAllTodos": get_all_todos,
    "createTodo": create_todo,
    "deleteTodoById": delete_todo_by_id,
    "searchTodo": search_todo,
}
