# Exploratory Windows helpers

These scripts record the auxiliary Windows networking and UDP work used while trying
to hand a WBR3 from its pairing AP to a local `cloudcutterflash` hotspot. They are kept
for research reproducibility and are **not** the recommended flashing route. Use Tuya
CloudCutter's maintained Linux workflow whenever possible.

## Contents

- `start-hotspot-async.ps1`, `stop-hotspot.ps1`, `hotspot-status.ps1`: manage and inspect
  the Windows mobile hotspot. The temporary public credentials are SSID
  `cloudcutterflash`, passphrase `abcdabcd`.
- `wifi-handoff-final.ps1`: associates with the device's open `A-7083` pairing AP,
  starts the temporary hotspot, and sends the Wi-Fi handoff packet.
- `send_cloudcutter_udp.py`: sends the exploratory Tuya UDP `exploit` or `wifi` packet.
  It is useful for documenting the protocol work, but it does not replace CloudCutter's
  profile-aware flashing flow.
- `dns_redirect.py`: minimal A-record responder used to steer the device during local
  bring-up.
- `tcp_forward.py`: bidirectional TCP forwarder for local service interception.
- `a-7083.xml`, `smartlife-7083.xml`, `wbr3-min.xml`: open WLAN profiles observed during
  bring-up. They contain no passwords.

Run PowerShell with permission to change network settings and Python 3 for the Python
helpers. Example:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-hotspot-async.ps1
python .\send_cloudcutter_udp.py wifi --ip 192.168.175.1
powershell -ExecutionPolicy Bypass -File .\stop-hotspot.ps1
```

Use only on hardware you own and on an isolated network. Do not import a real, password
protected WLAN profile into this public repository.
