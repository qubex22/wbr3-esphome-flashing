# Security notes

This repository intentionally excludes secrets and device-unique material.

- Never commit `secrets.yaml`, real WLAN profiles, device configuration exports,
  Tuya authorization keys, UUIDs, or flash dumps.
- Keep `backup/`, `*.dump`, and `stock.bin` out of Git. A stock flash dump can expose
  Wi-Fi credentials and Tuya cloud keys.
- The included hotspot passphrase and Wi-Fi configuration values are public examples
  for a temporary, isolated flashing network. Change them for any shared environment.
- The `send_cloudcutter_udp.py` helper implements the same type of device takeover
  handshake used during the research. Run it only against hardware you own and only
  on an isolated network.
- If a real credential is ever committed, rotate it immediately. Removing it in a new
  commit does not remove it from Git history.
