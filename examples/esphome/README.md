# ESPHome examples

## `wbr3-min.yaml`

The recovery-safe bootstrap used to build `artifacts/wbr3-min-image_firmware_is.0x010000.bin`.
It contains Wi-Fi fallback AP, captive portal, web server, native API, and ESPHome OTA,
but no fan/light entities. Set Wi-Fi values in `secrets.yaml`; use the example file as
the starting point.

Build and inspect the resulting binary before flashing:

```powershell
uvx --from esphome esphome compile .\wbr3-min.yaml
uvx ltchiptool flash file <esphome-build-directory>/rtl87xx/wbr3/.pio/build/wbr3-min/firmware.bin
```

ESPHome/LibreTiny emits both a UF2 and the application image. For CloudCutter, select
the AmebaZ2 `image_firmware_is.0x010000.bin` extracted from the build, not the UF2.

## Bring-up configurations

`plik-aura-bringup.yaml` and `create-windcalm-bringup.yaml` are diagnostic configurations
for observing the Tuya datapoint stream and testing candidate entities. They are not
ready-made final product definitions. Log `on_datapoint_update`, operate the physical
controls, and confirm each DP before trusting a writable entity.

The examples omit `build_path` so ESPHome uses its default local build directory.
