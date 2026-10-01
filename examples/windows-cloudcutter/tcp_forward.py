#!/usr/bin/env python3
import argparse
import asyncio


async def pipe(reader, writer):
    try:
        while True:
            data = await reader.read(65536)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except (ConnectionError, asyncio.CancelledError):
        pass
    finally:
        writer.close()


async def handle(client_reader, client_writer, target_host, target_port):
    try:
        remote_reader, remote_writer = await asyncio.open_connection(
            target_host, target_port
        )
    except OSError:
        client_writer.close()
        return
    await asyncio.gather(
        pipe(client_reader, remote_writer),
        pipe(remote_reader, client_writer),
    )


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--ports", default="80,443,4433,1883")
    args = parser.parse_args()

    servers = []
    for port_text in args.ports.split(","):
        port = int(port_text)
        server = await asyncio.start_server(
            lambda r, w, p=port: handle(r, w, args.target, p),
            "0.0.0.0",
            port,
        )
        servers.append(server)
    await asyncio.gather(*(server.serve_forever() for server in servers))


if __name__ == "__main__":
    asyncio.run(main())
