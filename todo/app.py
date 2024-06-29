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

db = Database("todo.db")


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


def render_todo(todo):
    return f"""
<div>
    {html.escape(todo["description"])}
</div>
"""


def render_home():
    rendered_todos = "\n".join(render_todo(todo) for todo in db["todos"].rows)
    return f"""
<div hx-target="this" hx-swap="outerHTML">
    {rendered_todos}
    <form hx-post="/">
        <input type="text" name="description" autofocus>
    </form>
</div>
"""


async def home(request: Request):
    return HTMLResponse(page(render_home(), "Todos"))


async def add_todo(request: Request):
    async with request.form() as form:
        db["todos"].insert({"description": form["description"]})
    return HTMLResponse(render_home())


routes = [
    Route("/", home, methods=["get"]),
    Route("/", add_todo, methods=["post"]),
]

if DEBUG:
    routes.append(LIVE_RELOAD_ROUTE)

app = Starlette(debug=DEBUG, routes=routes)
