from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket

# Adapted from: https://github.com/AnswerDotAI/fasthtml/blob/main/fasthtml/live_reload.py
# The idea is to inject a script that opens a websocket to `/live-reload` when the page loads.
# Before the server restarts (as `uvicorn --reload` does when a file is changed), it closes the socket.
# The page script listens for the close event and reloads the page.

LIVE_RELOAD_SCRIPT = """
<script>
    var socket = new WebSocket(`ws://${window.location.host}/live-reload`);
    socket.onclose = function(event) {
        if (event.wasClean) {
            window.location.reload();
        }
    }
</script>
"""


async def live_reload_endpoint(websocket: WebSocket):
    await websocket.accept()


LIVE_RELOAD_ROUTE = WebSocketRoute("/live-reload", endpoint=live_reload_endpoint)
