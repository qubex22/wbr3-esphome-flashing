# WBR3 bootstrap artifacts

`wbr3-min-image_firmware_is.0x010000.bin` is a minimal ESPHome/LibreTiny image
for the Tuya WBR3 board. It includes Wi-Fi fallback AP, captive portal, web
server, native API and ESPHome OTA, but no fan or light entities.

Intended use: flash this with Tuya CloudCutter as the first no-solder stage,
confirm network recovery, then upload a device-specific ESPHome configuration
over OTA. Confirm the exact fan model, Tuya PID, module firmware and CloudCutter
profile before flashing anything.

The file was built with ESPHome 2026.10.0-dev and LibreTiny 1.13.0. It was
identified by ltchiptool 4.14.4 as `Realtek AmebaZ2 Firmware` and contains the
RTL8720CF OTA signature expected by Tuya CloudCutter at byte offset 32.

## Files and integrity

| File | Use | SHA-256 |
|---|---|---|
| `wbr3-min-image_firmware_is.0x010000.bin` | CloudCutter AmebaZ2 OTA payload | `C4157F4D50A7D33AC5F2A2593D83735E47D3BFC94B459A5AEFDACBC6D8269295` |
| `wbr3-min-firmware.uf2` | ESPHome/LibreTiny UF2 packaging | `04247001BBAD17FDB0A02B8693C1BE767EA34DC3FF110E2C9F707DB524F775C7` |

Run `Get-FileHash .\wbr3-min-* -Algorithm SHA256` on Windows or
`sha256sum -c SHA256SUMS` on Linux before use. See [SHA256SUMS](SHA256SUMS).

The expected RTL8720CF OTA signature at bytes 32-47 is:

```text
68 51 3e f8 3e 39 6b 12 ba 05 9a 90 0f 36 b6 d3
```

Use the `.bin` for Tuya CloudCutter. The UF2 is retained for reproducibility and is not
accepted by the current CloudCutter UF2 selector for WBR3/RTL8720CF.
