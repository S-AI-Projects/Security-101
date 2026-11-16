import ipaddress
import json
from pathlib import Path

ALLOWLIST_CIDR = "192.0.2.0/24"


def classify_address(address, allowlist_cidr=ALLOWLIST_CIDR):
    try:
        ip = ipaddress.ip_address(address)
        network = ipaddress.ip_network(allowlist_cidr, strict=True)
    except ValueError:
        return {
            "input": address,
            "status": "REJECTED",
            "reason": "Malformed IP address or CIDR."
        }

    if ip.version != network.version:
        return {
            "input": address,
            "status": "DENIED",
            "reason": "Address and allowlist use different IP versions."
        }

    if ip in network:
        return {
            "input": address,
            "status": "ALLOWED",
            "reason": f"Address belongs to {network}."
        }

    return {
        "input": address,
        "status": "DENIED",
        "reason": f"Address does not belong to {network}."
    }


def main():
    fixture_path = Path(__file__).with_name("addresses.json")

    with fixture_path.open(encoding="utf-8") as fixture:
        addresses = json.load(fixture)

    for item in addresses:
        result = classify_address(item["input"])
        print(json.dumps(result))


if __name__ == "__main__":
    main()
