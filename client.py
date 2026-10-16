#!/usr/bin/env python3
"""Console client: fetch JSON from local API and print readable output."""
import sys
import json
import urllib.request


def fetch(url):
    with urllib.request.urlopen(url) as resp:
        if resp.getcode() != 200:
            raise RuntimeError(f"HTTP error: {resp.getcode()}")
        return json.load(resp)


def print_entry(entry):
    # entry expected to be a dict with optional 'title' and 'items'
    title = entry.get('title') or entry.get('id') or '<no title>'
    print(f"{title}")
    items = entry.get('items')
    if isinstance(items, list):
        for it in items:
            name = it.get('name') if isinstance(it, dict) else str(it)
            typ = it.get('type') if isinstance(it, dict) else ''
            if typ:
                print(f"  - {name} ({typ})")
            else:
                print(f"  - {name}")
    else:
        # print other fields in a compact way
        for k, v in entry.items():
            if k == 'items':
                continue
            print(f"  {k}: {v}")


def pretty_print(data):
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, dict):
                print_entry(entry)
                print()
            else:
                print(entry)
    elif isinstance(data, dict):
        print_entry(data)
    else:
        # unknown format: print raw JSON
        print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000/data'
    try:
        data = fetch(url)
        pretty_print(data)
    except Exception as e:
        print('Error fetching data:', e)


if __name__ == '__main__':
    main()
