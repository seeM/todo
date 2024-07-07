from dataclasses import dataclass

from fasthtml.common import FastHTML
from fasthtml.components import H1, Button, Div, Form, Input, Title

from .fastlite import Database


@dataclass
class Todo:
    id: int = None
    description: str = None

    def __xt__(self):
        return Div(self.description, Button("delete", hx_delete=f"/todos/{self.id}", hx_target="closest div"))


app = FastHTML()
db = Database("todo.sqlite")
todos = db.table("todos", Todo)


# TODO: may be nice if hx_swap_oob accepted bools too
def TodoInput(hx_swap_oob=""):
    return Input(id="todo-input", type="text", name="description", hx_swap_oob=hx_swap_oob)


@app.get("/")
def home():
    return (
        Title("Todos"),
        H1("Todos"),
        Div(*todos()),
        Form(TodoInput(), hx_target="this", hx_swap="beforebegin", hx_post="/todos"),
    )


@app.post("/todos")
def add_todo(todo: Todo):
    return todos.insert(todo, pk="id"), TodoInput(hx_swap_oob="true")


@app.delete("/todos/{id}")
def delete_todo(id: int):
    todos.delete(id)
    return ""
