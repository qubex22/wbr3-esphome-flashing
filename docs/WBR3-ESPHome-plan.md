# WBR3 ceiling fan: no-desolder ESPHome plan

## Recommendation

Use Tuya CloudCutter over Wi-Fi. Do not start with UART: a normal soldered WBR3
hides the two pins required for ROM download (`PA15/RX2` and the `PA00` download
strap) on the underside of the module.

The goal image for CloudCutter should be the ESPHome/LibreTiny AmebaZ2
`image_firmware_is.0x010000.bin`, not `firmware.uf2`. OpenBeken's WBR3 build
publishes its `firmware_is.bin` directly as the `*_ota.img`, and CloudCutter
recognizes that RTL8720CF OTA format. Validate the ESPHome artifact before use:

1. `uvx ltchiptool flash file image_firmware_is.0x010000.bin` must identify an
   AmebaZ2/RTL8720CF application/OTA image.
2. Bytes 32-47 must be `68 51 3e f8 3e 39 6b 12 ba 05 9a 90 0f 36 b6 d3`, the
   RTL8720CF OTA signature checked by current CloudCutter.

Do not give `firmware.uf2` to the current CloudCutter selector for this chip. Its
UF2 family map only contains BK7231T/N and its UF2 extractor assumes a
single-OTA Beken package; WBR3/RTL8720CF is dual-OTA.

## Phase 1: identify the exact device

Collect these before running the exploit:

- Exact fan/controller model and, if available, Tuya PID (`Product ID`).
- Photos of the WBR3 marking and the controller PCB.
- Tuya app -> device -> Device update: **Main module** and MCU versions.
- The pairing AP name and whether the LED gives a slow- or fast-blink pairing
  indication.

The PliK Aura Tuya model is `0000032byq`, PID `q6zofvaywu6imra4`. It is not in
the CloudCutter device catalog, but its DP schema is confirmed from the Tuya
developer platform:

| DP | Code | Type / range |
|---:|---|---|
| 20 | switch_led | bool |
| 21 | work_mode | enum white/colour/scene/music |
| 23 | temp_value | 0..1000 |
| 24 | colour_data | JSON string |
| 25 | scene_data | string |
| 28 | control_data | string |
| 58 | brightness_min_1 | 10..1000 |
| 59 | led_type_1 | enum led/incandescent/halogen |
| 60 | fan_switch | bool |
| 62 | fan_speed | 1..6 |
| 63 | fan_direction | enum forward/reverse |
| 64 | countdown_left_fan | 0..540 minutes |

The generic `rtl8720cf_common_user_config_ty` profiles are therefore the right
CloudCutter class once the module firmware version is confirmed. Two current
CloudCutter device profiles are useful cross-checks:

- `CREATE Windcalm DC Fan Light v2.5.2`: same six-speed/light architecture.
- `Carro CES523A2L1 Ceiling Fan v2.5.2` or `v2.1.6`: WBR3/TuyaMCU, but its
  published schema exposes three speeds, so it is less likely to be the exact
  six-speed product.

Profile selection must match the module firmware family/version. The PliK Aura
module is **2.1.6**, so the exact profile is
`rtl8720cf-common-user-config-ty-2.1.6-sdk-1.0.12-40.00`. Versions 2.6.3,
2.6.22, 2.7.7, 2.7.29, 3.1.23 and 3.1.69 are currently listed as patched and
cannot use the exploit.

## Phase 2: build the recovery-safe ESPHome image

Use `rtl87xx: board: wbr3`. The first image must contain `api`, `ota`,
`web_server`, `captive_portal`, and a fallback `wifi.ap`, so a bad Wi-Fi setting
or datapoint map remains recoverable over the network.

The fan MCU stays on the WBR3 UART0 pins:

| WBR3 pin | GPIO | Function |
|---|---|---|
| 15 | PA13 | UART0 RX, connect to MCU TX |
| 16 | PA14 | UART0 TX, connect to MCU RX |

Use 9600 baud for the likely `rtl8720cf_common_user_config_ty` TuyaMCU link.
Keep logger away from UART0.

For the PliK Aura schema, use these datapoints:

| DP | Type | Likely function |
|---:|---|---|
| 20 | bool | light power |
| 62 | value 1..6 | fan speed |
| 63 | enum | forward/reverse |
| 64 | value 0..540 | fan timer, minutes |
| 60 | bool | fan power |
| 21 | enum | white/colour/scene/music |
| 23 | value 0..1000 | cold/warm value |
| 58 | value 10..1000 | minimum brightness setting |
| 28 | string | likely scene/music data |

Treat this table as a hypothesis. First boot with diagnostic entities only, log
`on_datapoint_update`, operate the physical remote/app-equivalent controls, and
confirm every DP before exposing writable entities to Home Assistant.

## Phase 3: CloudCutter

Use a Linux host with Docker, NetworkManager and a supported USB Wi-Fi adapter.
Update CloudCutter immediately before use. Put only the target fan in pairing
mode and use the `-o <exact-AP-name>` option if other Tuya devices are nearby.

1. Choose **Flash 3rd Party Firmware**.
2. Select the exact device profile, or the matching firmware class/version only
   after confirming the module version.
3. Select the validated `image_firmware_is.0x010000.bin` from `custom-firmware/`.
4. Put the fan in AP mode. Follow CloudCutter's prompt to reboot and enter AP
   mode again; RTL8720CF requires that second reboot before the flash phase.
5. Wait for `/files/<image>` to report a complete upload, then wait for reboot.
6. Check for the ESPHome fallback AP and the device's web page/API.

CloudCutter writes the inactive application slot and retains the stock partition
table/bootloader. It also replaces Tuya cloud credentials in storage, so returning
to normal Tuya cloud operation is not guaranteed even if the stock app is later
restored.

## Phase 4: validate and finish

1. Restore normal Wi-Fi and confirm `web_server`, native API and OTA still work.
2. Confirm fan power, speeds 1 through 6 and stop with no writes to direction.
3. Confirm light power, brightness and color temperature.
4. Confirm direction and timer only after their DP types are observed.
5. Add the final `tuya.fan` and `tuya.light` entities, then test the physical
   remote and power-cycle behavior.

The fan's separate MCU and remote should continue to work because CloudCutter
only replaces the Wi-Fi module application, but test this before reinstalling
the canopy.

## UART fallback and limits

ROM flashing uses UART2:

| Adapter | WBR3 |
|---|---|
| RX | pin 11, PA16/TX2 |
| TX | underside pad PA15/RX2 |
| 3.3 V | pin 8, stable supply |
| GND | pin 9 |
| Download strap | underside pad PA00 to 3.3 V while resetting |

`PA13/RX0` must not be pulled low. Pulse CEN low or power-cycle after the strap
is high. On a standard soldered WBR3, RX2 and PA00 are inaccessible, so serial
flashing normally requires lifting the module. TX2 + GND alone is sufficient for
logs and possibly recovering Tuya keys, but not for ROM writes.

## Sources

- https://github.com/tuya-cloudcutter/tuya-cloudcutter
- https://github.com/tuya-cloudcutter/tuya-cloudcutter/wiki/Known-Patched-Firmware
- https://github.com/tuya-cloudcutter/tuya-cloudcutter/issues/706
- https://docs.libretiny.eu/boards/wbr3/
- https://docs.libretiny.eu/platform/realtek-ambz2/
- https://docs.libretiny.eu/projects/esphome/
- https://github.com/ardamaks/wbr3-flash
- https://github.com/openshwprojects/OpenBK7231T_App
- https://tuya-cloudcutter.github.io/api/devices/create-windcalm-dc-fan-light-v2.5.2.json
- https://tuya-cloudcutter.github.io/api/devices/carro-ces523a2l1-ceiling-fan-v2.5.2.json
