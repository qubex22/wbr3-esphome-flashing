#!/usr/bin/env python3
import argparse
import socket
import struct


def parse_question(data: bytes):
    offset = 12
    while offset < len(data) and data[offset] != 0:
        offset += data[offset] + 1
    if offset + 5 > len(data):
        return None
    return data[12:offset + 5], struct.unpack("!H", data[offset + 1:offset + 3])[0]


def make_response(data: bytes, address: str) -> bytes:
    question = parse_question(data)
    if not question or len(data) < 12:
        return b""
    query, qtype = question
    flags = 0x8180
    header = struct.pack("!HHHHHH", struct.unpack("!H", data[:2])[0], flags, 1, int(qtype == 1), 0, 0)
    if qtype != 1:
        return header + query
    answer = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 60, 4) + socket.inet_aton(address)
    return header + query + answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", default="192.168.137.1")
    parser.add_argument("--bind", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=53)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.bind, args.port))
    while True:
        data, peer = sock.recvfrom(4096)
        response = make_response(data, args.address)
        if response:
            sock.sendto(response, peer)


if __name__ == "__main__":
    main()
