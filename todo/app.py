from __future__ import annotations

import html
import os

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
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
    </head>
    <body>
        {body}
    </body>
</html>
"""


async def home(request: Request):
    rendered_todos = "\n".join(f"<div>{html.escape(todo)}</div>" for todo in todos)
    form = """
<form action="/" method="post">
    <input type="text" name="todo">
</form>
"""
    body = rendered_todos + form
    return HTMLResponse(page(body, "My Page"))


async def add_todo(request: Request):
    async with request.form() as form:
        todo = form["todo"]
        todos.append(todo)
    return RedirectResponse("/", status_code=302)


routes = [
    Route("/", home, methods=["get"]),
    Route("/", add_todo, methods=["post"]),
]

if DEBUG:
    routes.append(LIVE_RELOAD_ROUTE)

app = Starlette(debug=DEBUG, routes=routes)
