# Research provenance

The process was developed against the following upstream revisions. These are pinned
because profile catalogs and exploit compatibility change over time.

| Project | Revision | Purpose |
|---|---|---|
| [tuya-cloudcutter](https://github.com/tuya-cloudcutter/tuya-cloudcutter) | `971aa3d4863b4b5d819b62739090114da8f15e38` | OTA exploit, firmware/profile selection, RTL8720CF OTA handling |
| [tuya-cloudcutter wiki](https://github.com/tuya-cloudcutter/tuya-cloudcutter.wiki) | `8254efb666173e837afb92e434ae805b55c3e4d7` | patched-firmware and troubleshooting notes |
| [ltchiptool](https://github.com/libretiny-eu/ltchiptool) | `9fee418eeae52e5e38a91f3ed63c24cb25b5fb93` | AmebaZ2 image identification and flash tooling |
| [wbr3-flash](https://github.com/ardamaks/wbr3-flash) | `9cf3e5f64532040f3de8fa54ab4f05fce3524984` | WBR3 board research, boot layout, UART and TuyaMCU findings |
| [esphome-kickstart](https://github.com/libretiny-eu/esphome-kickstart) | `759b5db2ffd7911af3832f1e91fa9df3aa81aa5a` | LibreTiny ESPHome bootstrap patterns |

Additional references:

- LibreTiny [WBR3 board documentation](https://docs.libretiny.eu/boards/wbr3/)
- LibreTiny [Realtek AmebaZ2 platform](https://docs.libretiny.eu/platform/realtek-ambz2/)
- LibreTiny [ESPHome project documentation](https://docs.libretiny.eu/projects/esphome/)
- CloudCutter [Known Patched Firmware](https://github.com/tuya-cloudcutter/tuya-cloudcutter/wiki/Known-Patched-Firmware)
- CloudCutter issue [#706](https://github.com/tuya-cloudcutter/tuya-cloudcutter/issues/706)
- CREATE Windcalm profile: `rtl8720cf-common-user-config-ty-2.5.2-sdk-1.0.12-40.00`
- Carro CES523A2L1 profiles: `rtl8720cf-common-user-config-ty-2.5.2-sdk-1.0.12-40.00`
  and `rtl8720cf-common-user-config-ty-2.1.6-sdk-1.0.12-40.00`

The CREATE and Carro profiles were cross-checks for firmware-family selection, not
validated substitutes for the PliK Aura device. The documented PliK Aura module uses
`rtl8720cf-common-user-config-ty-2.1.6-sdk-1.0.12-40.00`.
