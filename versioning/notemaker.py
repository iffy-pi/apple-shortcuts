import sys
import os
import json

def main():
    startLineNo = int(sys.argv[1])
    endLineNo = int(sys.argv[2])

    with open('prerelease.md', 'r' ) as file:
        lines = file.readlines()

    selected = lines[startLineNo-1: endLineNo]

    dix = {
        'notes' : '\\n'.join([ l.rstrip() for l in selected])
    }

    print(json.dumps(dix))


if __name__ == "__main__":
    sys.exit(main())