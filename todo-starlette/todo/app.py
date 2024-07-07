from __future__ import annotations

import html
import os

from sqlite_utils import Database
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route

from .live_reload import LIVE_RELOAD_ROUTE, LIVE_RELOAD_SCRIPT

DEBUG = os.getenv("DEBUG")

db = Database("todo.sqlite")


def render_page(body: str, title: str):
    # TODO: It would be great if there was a single place to add features like live reload.
    #       Suspect that would need a custom application class.
    if DEBUG:
        body = LIVE_RELOAD_SCRIPT + body
    return f"""
<html>
    <head>
        <title>{title}</title>
        <script src="https://unpkg.com/htmx.org"></script>
    </head>
    <body>
        <h1>Todos</h1>
        {body}
    </body>
</html>
"""


def render_todo(todo):
    return f"""
<div>
    {html.escape(todo["description"])}
    <button hx-delete="/todos/{todo["id"]}" hx-target="closest div">delete</a>
</div>
"""


def render_input(hx_swap_oob=False):
    hx_swap_oob_attr = "hx-swap-oob=true" if hx_swap_oob else ""
    return f'<input id="todo-input" type="text" name="description" {hx_swap_oob_attr}>'


def render_home():
    rendered_todos = "\n".join(render_todo(todo) for todo in db["todos"].rows)
    return f"""
<div>
    {rendered_todos}
    <form hx-target="this" hx-swap="beforebegin" hx-post="/todos">
        {render_input()}
    </form>
</div>
"""


async def home(request: Request):
    return HTMLResponse(render_page(render_home(), "Todos"))


async def add_todo(request: Request):
    async with request.form() as form:
        todo = {"description": form["description"]}
    todo["id"] = db["todos"].insert(todo).last_pk
    content = render_todo(todo) + render_input(hx_swap_oob=True)
    return HTMLResponse(content)


async def delete_todo(request: Request):
    db["todos"].delete(request.path_params["id"])
    return HTMLResponse()


routes = [
    Route("/", home, methods=["get"]),
    Route("/todos", add_todo, methods=["post"]),
    Route("/todos/{id:int}", delete_todo, methods=["delete"]),
]

if DEBUG:
    routes.append(LIVE_RELOAD_ROUTE)

app = Starlette(debug=DEBUG, routes=routes)
