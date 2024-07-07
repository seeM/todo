from fastcore.all import patch
from fasthtml.common import Database, FastHTML
from fasthtml.components import (
    H1,
    Button,
    Div,
    Form,
    Input,
    Title,
)

app = FastHTML()
db = Database("todo.sqlite")
todos = db.t.todos
if todos not in db.t:
    todos.create(id=int, description=str, pk="id")
Todo = todos.dataclass()


def TodoInput(hx_swap_oob=False):
    kwargs = {"hx_swap_oob": "true"} if hx_swap_oob else {}
    return Input(id="todo-input", type="text", name="description", **kwargs)


@patch
def __xt__(self: Todo):  # type: ignore
    return Div(
        self.description,
        Button("delete", hx_delete=f"/todos/{self.id}", hx_target="closest div"),
    )


@app.get("/")
def home():
    print(Todo.__doc__)
    return (
        Title("Todos"),
        H1("Todos"),
        Div(*todos()),
        Form(
            TodoInput(),
            hx_target="this",
            hx_swap="beforebegin",
            hx_post="/todos",
        ),
    )


@app.post("/todos")
def add_todo(todo: Todo):  # type: ignore
    return todos.insert(todo, pk="id"), TodoInput(hx_swap_oob=True)


@app.delete("/todos/{id}")
def delete_todo(id: int):
    todos.delete(id)
    return ""
