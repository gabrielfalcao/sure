#!/Users/gabrielfalcao/projects/personal/HTTPretty/.venv/bin/python3
import sys
import json
from pathlib import Path
from sphinx.util.inventory import InventoryFile


def main():

    if len(sys.argv) < 2:
        print(f'USAGE:\n{sys.argv[0]} path/to/objects.inv')
        raise SystemExit(1)

    filename = Path(sys.argv[-1]).absolute()
    if not filename.exists():
        print(f'filename does not exist: {filename}')
        raise SystemExit(1)

    with filename.open('rb') as fd:
        inventory = InventoryFile.load(fd, "https://chemist.readthedocs.io/en/latest", lambda k, v: "/".join([k, v]))

    print(json.dumps(inventory, indent=2))

if __name__ == '__main__':
    main()
