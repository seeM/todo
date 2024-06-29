from __future__ import annotations

import html
import os

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route

from .live_reload import LIVE_RELOAD_ROUTE, LIVE_RELOAD_SCRIPT

DEBUG = os.getenv("DEBUG")


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
    todos = [
        "render a list of todos",
        "add a todo",
        "delete a todo",
        "</li><script>console.log('Im in!')</script>",
    ]
    rendered_todos = "\n".join(f"<li>{html.escape(todo)}</li>" for todo in todos)
    body = f"<ul>{rendered_todos}</ul>"
    return HTMLResponse(page(body, "My Page"))


routes = [
    Route("/", home),
]

if DEBUG:
    routes.append(LIVE_RELOAD_ROUTE)

app = Starlette(debug=DEBUG, routes=routes)
