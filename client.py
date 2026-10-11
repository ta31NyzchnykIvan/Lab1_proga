#!/usr/bin/env python3
"""Simple console client that fetches JSON from local API and prints it."""
import sys
import json
import urllib.request


def fetch(url):
    with urllib.request.urlopen(url) as resp:
        if resp.getcode() != 200:
            raise RuntimeError(f"HTTP error: {resp.getcode()}")
        return json.load(resp)


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000/data'
    try:
        data = fetch(url)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print('Error fetching data:', e)


if __name__ == '__main__':
    main()
