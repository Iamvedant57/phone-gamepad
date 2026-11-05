"""
Phone Gamepad server (Windows).
Serves the controller page to your phone and turns its input into a
virtual Xbox 360 controller that games recognise.

Run:  python server.py
Then open the printed address on your phone (same Wi-Fi).
"""
import json
import socket
from pathlib import Path

from aiohttp import web, WSMsgType
import vgamepad as vg

PORT = 8765
HERE = Path(__file__).parent

pad = vg.VX360Gamepad()
B = vg.XUSB_BUTTON

BUTTONS = {
    "a": B.XUSB_GAMEPAD_A,
    "b": B.XUSB_GAMEPAD_B,
    "x": B.XUSB_GAMEPAD_X,
    "y": B.XUSB_GAMEPAD_Y,
    "lb": B.XUSB_GAMEPAD_LEFT_SHOULDER,
    "rb": B.XUSB_GAMEPAD_RIGHT_SHOULDER,
    "start": B.XUSB_GAMEPAD_START,
    "back": B.XUSB_GAMEPAD_BACK,
    "up": B.XUSB_GAMEPAD_DPAD_UP,
    "down": B.XUSB_GAMEPAD_DPAD_DOWN,
    "left": B.XUSB_GAMEPAD_DPAD_LEFT,
    "right": B.XUSB_GAMEPAD_DPAD_RIGHT,
}

held = set()


def clamp(v, lo, hi):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return 0.0
    return max(lo, min(hi, v))


def apply(state):
    pad.left_joystick_float(
        x_value_float=clamp(state.get("steer", 0), -1, 1), y_value_float=0.0
    )
    pad.left_trigger_float(value_float=clamp(state.get("lt", 0), 0, 1))
    pad.right_trigger_float(value_float=clamp(state.get("rt", 0), 0, 1))

    pressed = {k for k in state.get("buttons", []) if k in BUTTONS}
    for k in pressed - held:
        pad.press_button(button=BUTTONS[k])
    for k in held - pressed:
        pad.release_button(button=BUTTONS[k])
    held.clear()
    held.update(pressed)
    pad.update()


def reset_pad():
    held.clear()
    pad.reset()
    pad.update()


async def index(request):
    return web.FileResponse(HERE / "controller.html")


async def ws_handler(request):
    ws = web.WebSocketResponse(heartbeat=10)
    await ws.prepare(request)
    print("Phone connected:", request.remote)
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                try:
                    apply(json.loads(msg.data))
                except json.JSONDecodeError:
                    pass
    finally:
        reset_pad()  # never leave a stuck throttle if the phone drops
        print("Phone disconnected")
    return ws


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # no packet is sent; just picks the LAN interface
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def main():
    app = web.Application()
    app.add_routes([web.get("/", index), web.get("/ws", ws_handler)])
    print(f"\nOpen this on your phone:  http://{local_ip()}:{PORT}\n")
    web.run_app(app, host="0.0.0.0", port=PORT, print=None)


if __name__ == "__main__":
    main()
