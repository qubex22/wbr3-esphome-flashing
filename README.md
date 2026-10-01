# Tuya WBR3 no-solder flashing guide

This repository documents a reproducible route for replacing the Tuya firmware on a
Tuya **WBR3** module with **ESPHome / LibreTiny**, without desoldering the module. It
includes the research notes, a recovery-safe ESPHome bootstrap configuration, the
validated bootstrap firmware, and the auxiliary scripts used during bring-up.

The documented target is a PliK Aura ceiling fan controller with a WBR3 module and a
TuyaMCU fan/light controller. The WBR3 findings also apply to other WBR3 devices, but
the Tuya datapoint map is device-specific and must be confirmed on every model.

## What is in this repository

- [Flash plan](docs/WBR3-ESPHome-plan.md) - decision record, hardware findings,
  CloudCutter procedure, validation steps, and UART fallback.
- [Firmware artifacts](artifacts/README.md) - bootstrap image and SHA-256 checksums.
- [ESPHome examples](examples/esphome/README.md) - recovery-safe bootstrap and
  diagnostic fan/light bring-up configurations.
- [Windows helpers](examples/windows-cloudcutter/README.md) - exploratory hotspot,
  UDP, and network-handoff scripts from the bring-up session. The supported process is
  Tuya CloudCutter on Linux.
- [Research provenance](docs/research-provenance.md) - upstream repositories and the
  exact revisions consulted.

## Recommended route

Use Tuya CloudCutter's OTA exploit with the validated AmebaZ2 OTA image. UART flashing
is a fallback only: WBR3's RX2 and download-strap pads are underneath a normally
soldered module, so serial flashing requires lifting it.

1. Record the exact product model, Tuya PID, Wi-Fi module version, MCU version, and
   pairing AP name.
2. Check that the module firmware version is not in CloudCutter's patched-firmware
   list. The documented PliK Aura module is `2.1.6`.
3. Validate the bootstrap image and note its SHA-256 hash.
4. Prepare a recovery-safe ESPHome configuration with `api`, `ota`, `web_server`,
   `captive_portal`, and a fallback `wifi.ap`.
5. Update Tuya CloudCutter immediately before use. Put only the target device in
   pairing mode and select the exact module firmware/profile match.
6. Flash `artifacts/wbr3-min-image_firmware_is.0x010000.bin` with CloudCutter.
7. Connect to the fallback AP, verify web/API/OTA recovery, then deploy the
   device-specific configuration over OTA.
8. Discover the TuyaMCU datapoints from logs before enabling writable fan or light
   controls. Test the physical remote and power-cycle behavior before reinstalling.

The complete commands, pin maps, expected datapoints, and checks are in the
[flash plan](docs/WBR3-ESPHome-plan.md).

## Safety and compatibility

- This is an experimental firmware-modification procedure. A failed flash can require
  desoldering and UART recovery.
- Disconnect mains power before opening the controller. The carrier board contains
  live-mains circuitry.
- Do not publish or share a flash dump. It can contain Wi-Fi credentials and Tuya
  device keys.
- CloudCutter writes the inactive application slot and replaces Tuya cloud
  credentials in storage. Returning to normal Tuya cloud operation is not guaranteed.
- Confirm profile and firmware-version compatibility before every flash. Versions
  listed as patched by Tuya CloudCutter cannot use the exploit.
- The UF2 file is included for completeness. Do **not** feed it to the current
  CloudCutter UF2 selector for WBR3/RTL8720CF; use the `.bin` OTA image documented
  here.

## Repository policy

Third-party tools are referenced rather than vendored. No real Wi-Fi credentials,
flash dumps, Tuya keys, generated build trees, or dependency caches are committed.
See [SECURITY.md](SECURITY.md) before publishing changes.
