from __future__ import annotations

import html
import os

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route

from .live_reload import LIVE_RELOAD_ROUTE, LIVE_RELOAD_SCRIPT

DEBUG = os.getenv("DEBUG")

todos = [
    "render a list of todos",
    "add a todo",
    "delete a todo",
    "<script>console.log('Im in!')</script>",
]


def page(body: str, title: str):
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
        {body}
    </body>
</html>
"""


def render_todo(todo: str):
    return f"""
<div>
    {html.escape(todo)}
</div>
"""


def render_home():
    rendered_todos = "\n".join(render_todo(todo) for todo in todos)
    return f"""
<div hx-target="this" hx-swap="outerHTML">
    {rendered_todos}
    <form hx-post="/">
        <input type="text" name="todo" autofocus>
    </form>
</div>
"""


async def home(request: Request):
    return HTMLResponse(page(render_home(), "Todos"))


async def add_todo(request: Request):
    async with request.form() as form:
        todo = form["todo"]
        todos.append(todo)
    return HTMLResponse(render_home())


routes = [
    Route("/", home, methods=["get"]),
    Route("/", add_todo, methods=["post"]),
]

if DEBUG:
    routes.append(LIVE_RELOAD_ROUTE)

app = Starlette(debug=DEBUG, routes=routes)
