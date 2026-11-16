#!/usr/bin/env python3
"""Fetch the official Cengel appendix into an ignored local cache; optionally render a table."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--table', help='e.g. A-13')
    parser.add_argument('--render', action='store_true', help='Render actual selected pages; requires Poppler pdftoppm')
    args = parser.parse_args()
    meta = json.loads((ROOT/'tables/source.json').read_text())
    pages = meta['table_pages'].get(args.table, []) if args.table else []
    if args.table and not pages:
        parser.error('Unknown table ID')
    if args.render and not args.table:
        parser.error('--render requires --table')
    cache = ROOT/'.cache'
    cache.mkdir(exist_ok=True)
    pdf = cache/'cengel_si_8e.pdf'
    expected = meta['pdf_sha256']
    if not pdf.exists():
        request = Request(meta['pdf_url'], headers={'User-Agent':'ENS202-study-reference'})
        with urlopen(request, timeout=60) as response:
            payload = response.read()
        if not payload.startswith(b'%PDF-') or hashlib.sha256(payload).hexdigest() != expected:
            raise RuntimeError('Publisher document changed or is not the verified PDF; reverify before use.')
        pdf.write_bytes(payload)
    if hashlib.sha256(pdf.read_bytes()).hexdigest() != expected:
        raise RuntimeError('Cached PDF hash mismatch; reverify the source.')
    images = []
    if args.render:
        binary = shutil.which('pdftoppm')
        if not binary:
            raise RuntimeError('pdftoppm is missing; install Poppler to render original table pages.')
        for page in pages:
            prefix = cache/f'cengel-{args.table}-page-{page}'
            subprocess.run([binary,'-f',str(page),'-l',str(page),'-singlefile','-scale-to','2200','-png',str(pdf),str(prefix)],check=True)
            images.append(str(prefix)+'.png')
    print(json.dumps({'official_pdf':str(pdf),'table':args.table,'pdf_pages':pages,'page_images':images,'note':'Attach the actual page images to the model. Paths or links alone do not attach content. Check headers, columns and negative signs.'},indent=2))

if __name__ == '__main__':
    main()
