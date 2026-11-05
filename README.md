# Phone Gamepad (Windows)

Turns your phone into a wireless Xbox 360 controller for your PC.

## Setup
1. Install Python 3.9+.
2. `pip install -r requirements.txt`
   (vgamepad's installer will offer to install the ViGEmBus driver. Accept it and reboot if asked.
   If it doesn't, install ViGEmBus from https://github.com/nefarius/ViGEmBus/releases)
3. `python server.py`
4. On your phone (same Wi-Fi), open the address it prints, e.g. `http://192.168.1.23:8765`
5. Turn the phone sideways. Test at https://hardwaretester.com/gamepad before launching a game.

## Controls
- Left slider = left trigger (brake). Right slider = right trigger (gas).
- Centre pad = left stick, X axis (steering). Drag sideways; it springs back.
- Face buttons, D-pad, LB/RB, Start/Back = standard Xbox buttons.

## Notes
- If Windows Firewall asks, allow Python on private networks.
- Tilt steering needs https on most phones, so touch steering is the default.
- Mac: vgamepad is Windows-only; ask for a keyboard-mapping version instead.
