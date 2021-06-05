from collections import defaultdict
import logging
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from server import session as sessionlib

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
app = FastAPI()


@app.get("/")
async def index():
    return HTMLResponse(open("html/index.html").read())


async def broadcast(event: dict, session: dict):
    for username, details in session.items():
        await details["sock"].send_json(event)


@app.websocket("/ws/session")
async def websocket_endpoint(websocket: WebSocket):
    logging.debug("## New Incoming connection")
    await websocket.accept()
    while True:
        event = await websocket.receive_json()
        logging.debug("Got event - %s", event)
        in_session = event["data"].get("session")
        if event["event"] == "JoinSessionEvent":
            sessionlib.active_sessions[in_session["id"]][in_session["username"]] = {
                "sock": websocket
            }
            logging.debug("Updated session - %s", event)
            broadcast_event = {
                "event": "SessionUpdateEvent",
                "data": {
                    "session": {
                        "id": in_session["id"],
                        "username": in_session["username"],
                    },
                    "message": f"New Player joined {in_session['username']}",
                    "players": list(sessionlib.active_sessions.keys()),
                },
            }
            await broadcast(
                broadcast_event,
                session=sessionlib.active_sessions.get(in_session["id"]),
            )
            logging.debug("Broadcasted - %s", broadcast_event)
        if event["event"] == "GameEvent":
            logging.debug("Game event")
            msg = event["data"]["message"]
            session = sessionlib.active_sessions.get(in_session["id"])
            if in_session["username"] in session:
                broadcast_event = {
                    "event": "GameEvent",
                    "data": {"message": "msg", "username": in_session["username"]},
                }
                await broadcast(broadcast_event, session)
                logging.debug("Broadcasted - %s", broadcast_event)
            else:
                logging.error("Username not there")
        else:
            logging.warning("Unknown event %s", event)
