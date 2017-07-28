"""
build.py - Build a doc map file from the Elixir HTML docs.
"""
import pickle
import pathlib
import sys

def main(docpath):
    data = []
    bytecount = 0

    p = pathlib.Path(docpath)
    for el in p.glob('*/*'):
        if not el.is_file():
            continue

        if not str(el).endswith('html'):
            continue

        raw = el.read_text()

        data.append({
            'name': str(el).replace(docpath, ''),
            'data': raw.lower(),
        })

        bytecount += len(raw)

    print(f'Added {len(data)} entries, {bytecount / 1024 / 1024:.2}MB')

    pickle.dump(data, open('server.map', 'wb'))

if __name__ == '__main__':
    main(sys.argv[1])

