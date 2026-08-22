from __future__ import annotations

import argparse
import ipaddress

import uvicorn


def loopback_host(value: str) -> str:
    try:
        address = ipaddress.ip_address(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Brain Lab host must be a loopback IP") from exc
    if not address.is_loopback:
        raise argparse.ArgumentTypeError("Brain Lab supports loopback addresses only")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local-only SparkBrain Brain Lab")
    parser.add_argument("--host", type=loopback_host, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    uvicorn.run("sparkbrain.lab.app:app", host=args.host, port=args.port, reload=False)


if __name__ == "__main__":
    main()
